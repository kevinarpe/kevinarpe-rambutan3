import enum
import selectors
from subprocess import Popen
import subprocess
from subprocess import SubprocessError
from subprocess import TimeoutExpired
import signal
import time

import copy
import errno

from io import BufferedWriter, IOBase, BufferedReader, TextIOWrapper
import os

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.ANY import ANY
from rambutan3.check_args.annotation.ANY_VALUE_OF import ANY_VALUE_OF
from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.BYTEARRAY import BYTEARRAY
from rambutan3.check_args.annotation.BYTES import BYTES
from rambutan3.check_args.annotation.DICT_OF import DICT_OF
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INPUT_STREAM import INPUT_STREAM
from rambutan3.check_args.annotation.INSTANCE_BY_TYPE_NAME import INSTANCE_BY_TYPE_NAME
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.NON_EMPTY_SEQUENCE_OF import NON_EMPTY_SEQUENCE_OF
from rambutan3.check_args.annotation.NON_EMPTY_STR import NON_EMPTY_STR
from rambutan3.check_args.annotation.NON_EMPTY_TUPLE_OF import NON_EMPTY_TUPLE_OF
from rambutan3.check_args.annotation.NON_NEGATIVE_FLOAT import NON_NEGATIVE_FLOAT
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT
from rambutan3.check_args.annotation.OUTPUT_STREAM import OUTPUT_STREAM
from rambutan3.check_args.annotation.POSITIVE_NUMBER import POSITIVE_NUMBER
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SEQUENCE_OF import SEQUENCE_OF
from rambutan3.check_args.annotation.STR import STR
from rambutan3.container.RUnmodifiableDictView import RUnmodifiableDictView
from rambutan3.enumeration.REnum import REnum
from rambutan3.op_sys import RThreading
from rambutan3.op_sys.RSignalEnum import RSignalEnum




# SUBPROCESS = INSTANCE_OF(Popen)

# without capture
# with redirect-like capture
# with tee-like capture


class TimeoutExpiredError(SubprocessError):
    pass


class RSubprocessPipelineCommunicator:

    @check_args
    def __init__(self: SELF(),
                 *,
                 input_stream: INPUT_STREAM | NONE=None,
                 input_data: BYTES | BYTEARRAY | STR | NONE=None,
                 output_stream_seq: SEQUENCE_OF(OUTPUT_STREAM)=tuple()):
        """
        :type input_stream: IOBase
        :type output_stream_seq: list[IOBase]
        """

        if BYTEARRAY.matches(input_data):
            input_data = bytes(input_data)

        self.__optional_input_stream = input_stream
        self.__optional_input_data = input_data
        self.__optional_input_data_offset = 0
        self.__optional_output_stream_tuple = tuple(output_stream_seq)
        self.__is_communication_started = False
        self.__output_stream_to_output_dict = {}

    @check_args
    def communicate(self: SELF(),
                    *,
                    timeout_seconds: POSITIVE_NUMBER | NONE=None) \
            -> DICT_OF(key_matcher=OUTPUT_STREAM, value_matcher=BYTES | STR):

        if timeout_seconds is None \
        and not self.__is_communication_started \
        and self.__has_exactly_one_stream():

            if self.__optional_input_stream:
                if self.__optional_input_data:
                    try:
                        self.__optional_input_stream.write(self.__optional_input_data)
                    except OSError as e:
                        if errno.EPIPE != e.errno and errno.EINVAL != e.errno:
                            raise

                self.__optional_input_stream.close()

            else:
                # This is a trick: tuple has exactly one item.
                for output_stream in self.__optional_output_stream_tuple:
                    output_bytes_or_str = subprocess._eintr_retry_call(output_stream.read)
                    self.__output_stream_to_output_dict[output_stream] = output_bytes_or_str



            # TODO: What about self.wait() here?

        else:
            if timeout_seconds is not None:
                now = subprocess._time()
                endtime = now + timeout_seconds
            else:
                endtime = None

            try:
                self._communicate(endtime, timeout_seconds)
            finally:
                self.__is_communication_started = True

            sts = self.wait(timeout=self.__remaining_time(endtime))

        return self.__output_stream_to_output_dict


    def __has_exactly_one_stream(self):
        if self.__optional_input_stream is not None \
        and 0 == len(self.__optional_output_stream_tuple):
            return True

        if self.__optional_input_stream is None \
        and 1 == len(self.__optional_output_stream_tuple):
            return True

        return False


    if not subprocess.mswindows:
        # POSIX methods

        @check_args
        def _communicate(self: SELF(), endtime: FLOAT | NONE, orig_timeout_seconds: FLOAT):
            if self.__optional_input_stream and not self.__is_communication_started:
                # Flush stdio buffer.  This might block, if the user has
                # been writing to .stdin in an uncontrolled fashion.
                self.__optional_input_stream.flush()

                if not self.__optional_input_data:
                    self.__optional_input_stream.close()

            # Only create this mapping if we haven't already.
            if not self.__is_communication_started:
                for output_stream in self.__optional_output_stream_tuple:
                    self.__output_stream_to_output_dict[output_stream] = []

            # self.__save_input()

            if self.__optional_input_data:
                input_data_view = memoryview(self.__optional_input_data)

            with subprocess._PopenSelector() as selector:

                if self.__optional_input_stream and self.__optional_input_data:
                    selector.register(self.__optional_input_stream, selectors.EVENT_WRITE)

                for output_stream in self.__optional_output_stream_tuple:
                    selector.register(output_stream, selectors.EVENT_READ)

                timeout_seconds = None

                while selector.get_map():
                    if endtime:
                        timeout_seconds = self.__remaining_time(endtime)
                        if timeout_seconds < 0:
                            raise TimeoutExpiredError('Timed out after {} seconds'.format(orig_timeout_seconds))

                    ready_tuple_list = selector.select(timeout_seconds)
                    self.__check_timeout(endtime, orig_timeout_seconds)

                    # XXX Rewrite these to use non-blocking I/O on the file
                    # objects; they are no longer using C stdio!

                    for selector_key, events in ready_tuple_list:

                        if selector_key.fileobj is self.__optional_input_stream:

                            chunk = input_data_view[self.__optional_input_data_offset :
                                                    self.__optional_input_data_offset + subprocess._PIPE_BUF]
                            try:
                                count = os.write(selector_key.fd, chunk)
                                self.__optional_input_data_offset += count
                            except OSError as e:
                                if e.errno == errno.EPIPE:
                                    selector.unregister(selector_key.fileobj)
                                    selector_key.fileobj.close()
                                else:
                                    raise
                            else:
                                if self.__optional_input_data_offset >= len(self.__optional_input_data):
                                    selector.unregister(selector_key.fileobj)
                                    selector_key.fileobj.close()

                        else:
                            data = os.read(selector_key.fd, 32768)
                            if data:
                                output_list = self.__output_stream_to_output_dict[selector_key.fileobj]
                                output_list.append(data)
                            else:
                                selector.unregister(selector_key.fileobj)
                                selector_key.fileobj.close()

            self.wait(timeout=self.__remaining_time(endtime))

            # All data exchanged.  Translate lists into strings.
            for output_stream in self.__output_stream_to_output_dict:
                output_list = self.__output_stream_to_output_dict[output_stream]
                output_bytes = b''.join(output_list)
                self.__output_stream_to_output_dict[output_stream] = output_bytes

            # Translate newlines, if requested.
            # This also turns bytes into strings.
            if self.universal_newlines:
                if stdout is not None:
                    stdout = self._translate_newlines(stdout,
                                                      self.stdout.encoding)
                if stderr is not None:
                    stderr = self._translate_newlines(stderr,
                                                      self.stderr.encoding)

            return (stdout, stderr)


        def __save_input(self):
            # This method is called from the _communicate_with_*() methods
            # so that if we time out while communicating, we can continue
            # sending input if we retry.
            if self.__optional_input_stream and self._input is None:
                self.__optional_input_data_offset = 0
                self._input = input
                if self.universal_newlines and input is not None:
                    self._input = self._input.encode(self.__optional_input_stream.encoding)


    def __remaining_time(self, endtime):
        """Convenience for _communicate when computing timeouts."""
        if endtime is None:
            return None
        else:
            now = subprocess._time()
            x = endtime - now
            return x


    def __check_timeout(self, endtime, orig_timeout):
        """Convenience for checking if a timeout has expired."""
        if endtime is not None:
            now = subprocess._time()
            if now > endtime:
                raise TimeoutExpiredError(self.args, orig_timeout)


    def communicate(self, input=None, timeout=None):
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.  The optional input argument should be
        bytes to be sent to the child process, or None, if no data
        should be sent to the child.

        communicate() returns a tuple (stdout, stderr)."""

        if self._communication_started and input:
            raise ValueError("Cannot send input after starting communication")

        # Optimization: If we are not worried about timeouts, we haven't
        # started communicating, and we have one or zero pipes, using select()
        # or threads is unnecessary.
        if (timeout is None and not self._communication_started and
                    [self.stdin, self.stdout, self.stderr].count(None) >= 2):
            stdout = None
            stderr = None
            if self.stdin:
                if input:
                    try:
                        self.stdin.write(input)
                    except OSError as e:
                        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                            raise
                self.stdin.close()
            elif self.stdout:
                stdout = _eintr_retry_call(self.stdout.read)
                self.stdout.close()
            elif self.stderr:
                stderr = _eintr_retry_call(self.stderr.read)
                self.stderr.close()
            self.wait()
        else:
            if timeout is not None:
                endtime = _time() + timeout
            else:
                endtime = None

            try:
                stdout, stderr = self._communicate(input, endtime, timeout)
            finally:
                self._communication_started = True

            sts = self.wait(timeout=self.__remaining_time(endtime))

        return (stdout, stderr)



class RPopen(Popen):


    # input_data: "The type of input must be bytes..."
    def communicate(self,
                    *,
                    input_data=None,
                    timeout_seconds: POSITIVE_NUMBER | NONE=None,
                    extra_ostream_seq: SEQUENCE_OF(OUTPUT_STREAM)=tuple()):
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.  The optional input argument should be
        bytes to be sent to the child process, or None, if no data
        should be sent to the child.

        communicate() returns a tuple (stdout, stderr)."""

        if self._communication_started and input_data:
            raise ValueError("Cannot send input after starting communication")

        # Optimization: If we are not worried about timeouts, we haven't
        # started communicating, and we have one or zero pipes, using select()
        # or threads is unnecessary.

        if (timeout_seconds is None and not self._communication_started and
                    [self.stdin, self.stdout, self.stderr].count(None) >= 2):
            stdout = None
            stderr = None
            if self.stdin:
                if input_data:
                    try:
                        self.stdin.write(input_data)
                    except OSError as e:
                        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                            raise
                self.stdin.close()
            elif self.stdout:
                stdout = subprocess._eintr_retry_call(self.stdout.read)
                self.stdout.close()
            elif self.stderr:
                stderr = subprocess._eintr_retry_call(self.stderr.read)
                self.stderr.close()
                self.wait()
        else:
            if timeout_seconds is not None:
                endtime = subprocess._time() + timeout_seconds
            else:
                endtime = None

            try:
                stdout, stderr = self._communicate(input_data=input_data,
                                                   endtime=endtime,
                                                   orig_timeout_seconds=timeout_seconds,
                                                   extra_ostream_seq=extra_ostream_seq)
            finally:
                self._communication_started = True

            sts = self.wait(timeout=self._remaining_time(endtime))
        return (stdout, stderr)

    def _communicate(self,
                     *,
                     input_data,
                     endtime: FLOAT | NONE,
                     orig_timeout_seconds: POSITIVE_NUMBER | NONE,
                     extra_ostream_seq: SEQUENCE_OF(OUTPUT_STREAM)):

        # timeout_seconds: POSITIVE_NUMBER | NONE=None
        if self.stdin and not self._communication_started:
            # Flush stdio buffer.  This might block, if the user has
            # been writing to .stdin in an uncontrolled fashion.
            self.stdin.flush()
            if not input_data:
                self.stdin.close()

        # Only create this mapping if we haven't already.
        if not self._communication_started:
            self._fileobj2output = {}
            if self.stdout:
                self._fileobj2output[self.stdout] = []
            if self.stderr:
                self._fileobj2output[self.stderr] = []
            for extra_ostream in extra_ostream_seq:
                if extra_ostream is self.stdout:
                    # TODO: Throw?
                    pass

                if extra_ostream is self.stderr:
                    # TODO: Throw?
                    pass

                self._fileobj2output[extra_ostream] = []

        self._save_input(input_data)

        if self._input:
            input_view = memoryview(self._input)

        with subprocess._PopenSelector() as selector:
            if self.stdin and input_data:
                selector.register(self.stdin, selectors.EVENT_WRITE)
            for ostream in self._fileobj2output.keys():
                selector.register(ostream, selectors.EVENT_READ)

            while selector.get_map():
                timeout = self._remaining_time(endtime)
                if timeout is not None and timeout < 0:
                    raise subprocess.TimeoutExpired(self.args, orig_timeout_seconds)

                ready = selector.select(timeout)
                self._check_timeout(endtime, orig_timeout_seconds)

                # XXX Rewrite these to use non-blocking I/O on the file
                # objects; they are no longer using C stdio!

                for key, events in ready:
                    if key.fileobj is self.stdin:
                        chunk = input_view[self._input_offset :
                        self._input_offset + subprocess._PIPE_BUF]
                        try:
                            self._input_offset += os.write(key.fd, chunk)
                        except OSError as e:
                            if e.errno == errno.EPIPE:
                                selector.unregister(key.fileobj)
                                key.fileobj.close()
                            else:
                                raise
                        else:
                            if self._input_offset >= len(self._input):
                                selector.unregister(key.fileobj)
                                key.fileobj.close()
                    elif key.fileobj in (self.stdout, self.stderr):
                        data = os.read(key.fd, 32768)
                        if not data:
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                        self._fileobj2output[key.fileobj].append(data)

        self.wait(timeout=self._remaining_time(endtime))

        # All data exchanged.  Translate lists into strings.
        for ostream in self._fileobj2output.keys():
            bytes_list = self._fileobj2output[ostream]
            b = b''.join(bytes_list)

            # Translate newlines, if requested.
            # This also turns bytes into strings.
            if self.universal_newlines:
                b = self._translate_newlines(b, ostream.encoding)

            self._fileobj2output[ostream] = b

        x = dict(self._fileobj2output)
        return x


def pipe(p1_stdout_close_flag: BOOL):

    p1 = RPopen(args=['find', '/'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
    p2 = RPopen(args=['head', '-n', '1'], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if p1_stdout_close_flag:
        p1.stdout.close()

    stdout, stderr = p2.communicate()
    time.sleep(0.005)
    p1_exit_code = p1.poll()
    p2_exit_code = p2.poll()

    while p1_exit_code is None:
        print('p1_stdout_close_flag={}: p1: Send SIGTERM: {}'.format(p1_stdout_close_flag, time.monotonic()))
        p1.send_signal(signal.SIGTERM)
        time.sleep(0.005)
        p1_exit_code = p1.poll()

    print('p1_stdout_close_flag={}: p1_exit_code={}: stdout:[{}]'.format(p1_stdout_close_flag, p1_exit_code, stdout))


def main():
    pipe(p1_stdout_close_flag=True)
    return
    pipe(p1_stdout_close_flag=False)
    # p1 = Popen(args=['cat'], stdout=subprocess.PIPE, universal_newlines=True)

    p1 = Popen(args=['find', '/'], stdout=subprocess.PIPE, universal_newlines=True)
    p2 = Popen(args=['head', '-n', '1'], stdin=p1.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    p1.stdout.close()
    stdout, stderr = p2.communicate()
    p1_exit_code = p1.poll()
    p2_exit_code = p2.poll()

    while p1_exit_code is None:
        print('p1: Send SIGTERM: {}'.format(time.monotonic()))
        p1.send_signal(signal.SIGTERM)
        time.sleep(0.005)
        p1_exit_code = p1.poll()

    _p1 = Popen(args=['find', '/'], stdout=subprocess.PIPE, universal_newlines=True)
    _p2 = Popen(args=['head', '-n', '1'], stdin=_p1.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    # p1.stdout.close()
    _stdout, _stderr = _p2.communicate()
    _p1_exit_code = p1.poll()
    _p2_exit_code = p2.poll()

    s = open('../TODO.txt')
    r = s.readable()
    w = s.writable()
    s.close()
    s = open('../TODO.txt', mode='r')
    r = s.readable()
    w = s.writable()
    s.close()
    s = open('../TODO.txt', mode='r+')
    r = s.readable()
    w = s.writable()
    s.close()
    p = Popen(args=['ls', '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    x = p.stdin
    y = p.stdout
    p.communicate()

    # stdin
    # universal_newlines=False
    # (<class '_io.BufferedWriter'>, <class '_io._BufferedIOBase'>, <class '_io._IOBase'>, <class 'object'>)

    # universal_newlines=True
    # (<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)

    # stdout
    # universal_newlines=False
    # (<class '_io.BufferedReader'>, <class '_io._BufferedIOBase'>, <class '_io._IOBase'>, <class 'object'>)

    # universal_newlines=True
    # (<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)

    # @debug_breakpoint
    dummy = 1

if __name__ == "__main__":
    main()


@enum.unique
class RSubprocessStreamTypeEnum(REnum):

    DEVNULL = subprocess.DEVNULL
    PIPE = subprocess.PIPE
    STDOUT = subprocess.STDOUT


class RSubprocessSettings:

    __ARGS_IN = NON_EMPTY_SEQUENCE_OF(NON_EMPTY_STR)
    __ARGS_OUT = NON_EMPTY_TUPLE_OF(NON_EMPTY_STR)

    __STDIN = ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                           RSubprocessStreamTypeEnum.PIPE) \
              | OUTPUT_STREAM \
              | NONE

    __STDOUT = ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                            RSubprocessStreamTypeEnum.PIPE) \
               | INPUT_STREAM \
               | NONE

    __STDERR = ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                            RSubprocessStreamTypeEnum.PIPE,
                            RSubprocessStreamTypeEnum.STDOUT) \
               | INPUT_STREAM \
               | NONE

    __SHELL = BOOL

    __CWD = NON_EMPTY_STR | NONE

    __ENV_IN = DICT_OF(key_matcher=NON_EMPTY_STR, value_matcher=STR) | NONE

    __ENV_OUT = INSTANCE_OF(RUnmodifiableDictView)

    __UNIVERSAL_NEWLINES = BOOL

    @check_args
    def __init__(self: SELF(),
                 *,
                 args: __ARGS_IN,
                 stdin: __STDIN,
                 stdout: __STDOUT,
                 stderr: __STDERR,
                 shell: __SHELL,
                 cwd: __CWD,
                 env: __ENV_IN,
                 universal_newlines: __UNIVERSAL_NEWLINES):

        self.args = args
        self.__args_tuple = args
        self.__stdin = stdin
        self.__stdout = stdout
        self.__stderr = stderr
        self.__shell = shell
        self.__cwd = cwd
        self.__env = RUnmodifiableDictView(copy.copy(env))
        self.__universal_newlines = universal_newlines

    @check_args
    @property
    def args(self: SELF()) -> __ARGS_OUT:
        return self.__args_tuple

    # noinspection PyPropertyDefinition
    @check_args
    @args.setter
    def args(self: SELF(), new_args_seq: __ARGS_IN):
        self.__args_tuple = tuple(new_args_seq)

    @check_args
    @property
    def stdin(self: SELF()) -> __STDIN:
        return self.__stdin

    # noinspection PyPropertyDefinition
    @check_args
    @stdin.setter
    def stdin(self: SELF(), new_stdin: __STDIN):
        self.__stdin = new_stdin

    @check_args
    @property
    def raw_stdin(self: SELF()) -> INT | OUTPUT_STREAM | NONE:
        if isinstance(self.__stdin, RSubprocessStreamTypeEnum):
            x = self.__stdin.value
        else:
            x = self.__stdin

        return x

    @check_args
    @property
    def stdout(self: SELF()) -> __STDOUT:
        return self.__stdout

    # noinspection PyPropertyDefinition
    @check_args
    @stdout.setter
    def stdout(self: SELF(), new_stdout: __STDOUT):
        self.__stdout = new_stdout

    @check_args
    @property
    def raw_stdout(self: SELF()) -> INT | INPUT_STREAM | NONE:
        if isinstance(self.__stdout, RSubprocessStreamTypeEnum):
            x = self.__stdout.value
        else:
            x = self.__stdout

        return x

    @check_args
    @property
    def stderr(self: SELF()) -> __STDERR:
        return self.__stderr

    # noinspection PyPropertyDefinition
    @check_args
    @stderr.setter
    def stderr(self: SELF(), new_stderr: __STDERR):
        self.__stderr = new_stderr

    @check_args
    @property
    def raw_stderr(self: SELF()) -> INT | INPUT_STREAM | NONE:
        if isinstance(self.__stderr, RSubprocessStreamTypeEnum):
            x = self.__stderr.value
        else:
            x = self.__stderr

        return x

    @check_args
    @property
    def shell(self: SELF()) -> __SHELL:
        return self.__shell

    # noinspection PyPropertyDefinition
    @check_args
    @shell.setter
    def shell(self: SELF(), new_shell: __SHELL):
        self.__shell = new_shell

    @check_args
    @property
    def cwd(self: SELF()) -> __CWD:
        return self.__cwd

    # noinspection PyPropertyDefinition
    @check_args
    @cwd.setter
    def cwd(self: SELF(), new_cwd: __CWD):
        self.__cwd = new_cwd

    @check_args
    @property
    def env(self: SELF()) -> __ENV_OUT:
        return self.__env

    # noinspection PyPropertyDefinition
    @check_args
    @env.setter
    def env(self: SELF(), new_env: __ENV_IN):
        self.__env = new_env

    @check_args
    @property
    def universal_newlines(self: SELF()) -> __UNIVERSAL_NEWLINES:
        return self.__universal_newlines

    # noinspection PyPropertyDefinition
    @check_args
    @universal_newlines.setter
    def universal_newlines(self: SELF(), new_universal_newlines: __UNIVERSAL_NEWLINES):
        self.__universal_newlines = new_universal_newlines

    @check_args
    def __str__(self: SELF()) -> NON_EMPTY_STR:
        x = '{' \
            '\n    args: {},' \
            '\n    stdin: {},' \
            '\n    stdout: {},' \
            '\n    stderr: {},' \
            '\n    shell: {},' \
            '\n    cwd: {},' \
            '\n    env: {},' \
            '\n    universal_newlines: {}' \
            '\n}' \
            .format(self.__args_tuple, self.__stdin, self.__stdout, self.__stderr, self.__shell, self.__cwd, self.__env,
                    self.__universal_newlines)
        return x


# TODO: RImmutableSubprocessSettings


class RSubprocess:

    @check_args
    def __init__(self: SELF(), settings: INSTANCE_OF(RSubprocessSettings)):
        """:type settings: RSubprocessSettings"""
        # TODO: Use RImmutableSubprocessSettings here
        self.__settings = settings
        self.__process = subprocess.Popen(args=settings.args,
                                          stdin=settings.raw_stdin,
                                          stdout=settings.raw_stdout,
                                          stderr=settings.raw_stderr,
                                          shell=settings.shell,
                                          cwd=settings.cwd,
                                          env=settings.env,
                                          universal_newlines=settings.universal_newlines)

    @check_args
    @property
    def settings(self: SELF()) -> INSTANCE_OF(RSubprocessSettings):
        return self.__settings

    @check_args
    @property
    def stdin(self: SELF()) -> OUTPUT_STREAM:
        x = self.__process.stdin
        return x

    @check_args
    @property
    def stdout(self: SELF()) -> OUTPUT_STREAM:
        x = self.__process.stdout
        return x

    @check_args
    @property
    def stderr(self: SELF()) -> OUTPUT_STREAM:
        x = self.__process.stderr
        return x

    @check_args
    @property
    def returncode(self: SELF()) -> INT | NONE:
        x = self.__process.returncode
        return x

    @check_args
    def poll(self: SELF()) -> INT | NONE:
        x = self.__process.poll()
        return x

    @check_args
    def wait(self: SELF(),
             *,
             timeout_seconds: NON_NEGATIVE_FLOAT | NONE=None) -> INT:
        x = self.__process.wait(timeout=timeout_seconds)
        return x

    @check_args
    def wait_and_check_exit_code(self: SELF(),
                                 *,
                                 timeout_seconds: NON_NEGATIVE_FLOAT | NONE=None,
                                 valid_exit_code_seq: NON_EMPTY_SEQUENCE_OF(INT)=(0,)) \
            -> NON_EMPTY_TUPLE_OF(INT):
        exit_code = self.__process.wait()
        if exit_code not in valid_exit_code_seq:
            x = 'Invalid exit code ({}): Expected any of: {}' \
                '\n{}' \
                .format(exit_code, valid_exit_code_seq, self.__settings)
            raise RSubprocessExitCodeError(x)

    @check_args
    def send_signal(self: SELF(), signal_enum: INSTANCE_OF(RSignalEnum)):
        """:type signal_enum: RSignalEnum"""

        self.__process.send_signal(signal_enum.value)

    @check_args
    def terminate(self: SELF()):
        self.send_signal(RSignalEnum.SIGTERM)

    @check_args
    def kill(self: SELF()):
        self.send_signal(RSignalEnum.SIGKILL)


class RSubprocessBuilder:

    @check_args
    def __init__(self: SELF(),
                 *,
                 args: NON_EMPTY_SEQUENCE_OF(NON_EMPTY_STR),

                 stdin: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                     RSubprocessStreamTypeEnum.PIPE)
                        | INPUT_STREAM
                        | INSTANCE_BY_TYPE_NAME('RSubprocessBuilder')
                        | NONE=RSubprocessStreamTypeEnum.DEVNULL,

                 stdout: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                      RSubprocessStreamTypeEnum.PIPE)
                         | OUTPUT_STREAM | NONE=None,

                 stderr: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                      RSubprocessStreamTypeEnum.PIPE,
                                      RSubprocessStreamTypeEnum.STDOUT)
                         | OUTPUT_STREAM | NONE=None,

                 shell: BOOL=False,
                 cwd: NON_EMPTY_STR | NONE=None,
                 env: DICT_OF(key_matcher=NON_EMPTY_STR, value_matcher=STR) | NONE=None,
                 universal_newlines: BOOL=True):

        self.__settings = RSubprocessSettings(args=args, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd, env=env,
                                              universal_newlines=universal_newlines)

    # TODO: LAST: Do something about RSubprocessSettings.
    # Maybe RForwardingSubprocessSettings... then impl here?

    @check_args
    def start(self: SELF()) -> INSTANCE_OF(RSubprocess):
        x = RSubprocess(self.__settings)
        return x


class RSubprocessExitCodeError(SubprocessError):
    pass


class RSubprocessPipeline:

    # Refactor to use Subprocess internally

    @check_args
    def __init__(self: SELF(), settings_seq: NON_EMPTY_SEQUENCE_OF(INSTANCE_OF(RSubprocessSettings))):
        """:type settings_seq: list[RSubprocessSettings]"""

        # @debug
        self.__settings_list = copy.deepcopy([settings_seq])
        size = len(settings_seq)
        subprocess_list = [None] * size

        for i in range(size):
            settings = settings_seq[i]

            if i > 0:
                prev_process = subprocess_list[i - 1]
                settings.stdin = prev_process.stdout

            p = RSubprocess(settings)
            subprocess_list[i] = p

            if i > 0:
                prev_process = subprocess_list[i - 1]
                prev_process.stdout.close()

        self.__subprocess_tuple = tuple(subprocess_list)
        """:type: tuple[RSubprocess]"""
        self.__exit_code_tuple = None

    @check_args
    @property
    def subprocess_tuple(self: SELF()) -> NON_EMPTY_TUPLE_OF(INSTANCE_OF(RSubprocess)):
        return self.__subprocess_tuple

    @check_args
    def communicate(self: SELF(),
                    *,
                    input_data: BYTES | BYTEARRAY | STR | NONE=None,
                    timeout_seconds: POSITIVE_NUMBER | NONE=None):
        pass

    @check_args
    @property
    def returncodes(self: SELF()) -> NON_EMPTY_TUPLE_OF(INT) | NONE:
        return self.__exit_code_tuple

    @check_args
    def poll(self: SELF()) -> NON_EMPTY_TUPLE_OF(INT) | NONE:
        if self.__exit_code_tuple:
            return self.__exit_code_tuple

        exit_code_list = []
        for p in self.__subprocess_tuple:
            exit_code = p.poll()

            if exit_code is None:
                return None
            else:
                exit_code_list.append(exit_code)

        self.__exit_code_tuple = tuple(exit_code_list)
        return self.__exit_code_tuple

    @check_args
    def wait(self: SELF(),
             *,
             timeout_seconds: NON_NEGATIVE_FLOAT | NONE=None) -> NON_EMPTY_TUPLE_OF(INT):

        """Waits for each process in the pipeline to exit.

        Safe to call multiple times to retrieve exit code tuple.

        :param self:
        :param timeout_seconds:
        :return:

        @throws TimeoutExpired
                if {@code timeout_seconds} is not {@code None} and waiting period expires
        """
        if self.__exit_code_tuple:
            return self.__exit_code_tuple

        exit_code_list = []
        for p in self.__subprocess_tuple:
            exit_code = p.wait(timeout=timeout_seconds)
            exit_code_list.append(exit_code)

        self.__exit_code_tuple = tuple(exit_code_list)
        return self.__exit_code_tuple

    @check_args
    def wait_and_check_exit_codes(self: SELF(),
                                  *,
                                  timeout_seconds: NON_NEGATIVE_FLOAT | NONE=None,
                                  valid_exit_code_seq: NON_EMPTY_SEQUENCE_OF(NON_NEGATIVE_INT)=(0,)) \
            -> NON_EMPTY_TUPLE_OF(INT):

        """Waits for each process in the pipeline to exit.

        Safe to call multiple times to retrieve exit code tuple.

        :param self:
        :param timeout_seconds:
        :param valid_exit_code_seq:
        :return:
        @throws TimeoutExpired
                if {@code timeout_seconds} is not {@code None} and waiting period expires
        @throws SubprocessExitCodeError
                if any exit code is invalid
        """

        exit_code_tuple = self.wait(timeout_seconds=timeout_seconds)

        error = ''
        delim = ''
        size = len(exit_code_tuple)
        for i in range(size):
            exit_code = exit_code_tuple[i]
            if exit_code not in valid_exit_code_seq:
                if exit_code < 0:
                    signal_enum = RSignalEnum.try_find_member_by_value(-exit_code)
                    error += '{}Process {} of {}: Terminated by signal ({}: {})' \
                             '\n{}' \
                        .format(delim, 1 + i, size, -exit_code, signal_enum.name, self.__settings_list[i])
                else:
                    error += '{}Process {} of {}: Invalid exit code ({}): Expected any of: {}' \
                             '\n{}' \
                        .format(delim, 1 + i, size, exit_code, valid_exit_code_seq, self.__settings_list[i])
                delim = '\n'

        if error:
            raise RSubprocessExitCodeError(error)

        return exit_code_tuple

    @check_args
    def send_signal(self: SELF(), signal_enum: INSTANCE_OF(RSignalEnum)):
        """:type signal_enum: RSignalEnum"""

        for p in self.__subprocess_tuple:
            p.send_signal(signal_enum.value)

        # This microsleep is a trick to (greatly) increase the probability the signal will be processed by the receiver
        # by the time this method returns.
        time.sleep(RThreading.MICRO_SLEEP_SECONDS)

    @check_args
    def terminate(self: SELF()):
        self.send_signal(RSignalEnum.SIGTERM)

    @check_args
    def kill(self: SELF()):
        self.send_signal(RSignalEnum.SIGKILL)


class RSubprocessPipelineCommunicator2:

    @check_args
    def __init__(self: SELF(),
                 subprocess_pipeline: INSTANCE_OF(RSubprocessPipeline),
                 input_data: BYTES | BYTEARRAY | STR | NONE=None):
        """
        :type subprocess_pipeline: RSubprocessPipeline
        """

        # Do not directly modify reference for 'input_data'.
        input_data2 = input_data

        if BYTEARRAY.matches(input_data2):
            input_data2 = bytes(input_data2)

        subprocess0 = subprocess_pipeline.subprocess_tuple[0]
        if subprocess0.stdin:
            if input_data is not None and subprocess0.settings.universal_newlines:
                input_data2 = input_data2.encode(subprocess0.stdin.encoding)

        elif input_data is not None:
            raise ValueError('Cannot send input to STDIN')

        output_stream_list = []
        for subprocess in subprocess_pipeline.subprocess_tuple:
            if subprocess.stdout:
                output_stream_list.append(subprocess.stdout)

            if subprocess.stderr:
                output_stream_list.append(subprocess.stderr)

        self.__subprocess_pipeline = subprocess_pipeline
        self.__optional_input_stream = subprocess0.stdin
        self.__optional_input_data = input_data2
        self.__optional_input_data_offset = 0
        self.__output_stream_list = output_stream_list
        self.__is_communication_started = False
        self.__output_stream_to_output_dict = {}

    @check_args
    def communicate(self: SELF(),
                    *,
                    timeout_seconds: POSITIVE_NUMBER | NONE=None) \
            -> DICT_OF(key_matcher=OUTPUT_STREAM, value_matcher=BYTES | STR):

        if timeout_seconds is None \
                and not self.__is_communication_started \
                and self.__has_exactly_one_stream():

            subprocess0 = self.__subprocess_pipeline.subprocess_tuple[0]
            if subprocess0.stdin:
                if self.__optional_input_data:
                    try:
                        subprocess0.stdin.write(self.__optional_input_data)
                    except OSError as e:
                        if errno.EPIPE != e.errno and errno.EINVAL != e.errno:
                            raise

                subprocess0.stdin.close()

            else:
                for subprocess in self.__subprocess_pipeline.subprocess_tuple:
                    pass
                # This is a trick: tuple has exactly one item.
                for output_stream in self.__optional_output_stream_tuple:
                    output_bytes_or_str = subprocess._eintr_retry_call(output_stream.read)
                    self.__output_stream_to_output_dict[output_stream] = output_bytes_or_str



                    # TODO: What about self.wait() here?

        else:
            if timeout_seconds is not None:
                now = subprocess._time()
                endtime = now + timeout_seconds
            else:
                endtime = None

            try:
                self._communicate(endtime, timeout_seconds)
            finally:
                self.__is_communication_started = True

            sts = self.wait(timeout=self.__remaining_time(endtime))

        return self.__output_stream_to_output_dict


    def __has_exactly_one_stream(self):
        if self.__optional_input_stream is not None \
                and 0 == len(self.__output_stream_list):
            return True

        if self.__optional_input_stream is None \
                and 1 == len(self.__output_stream_list):
            return True

        return False


    if not subprocess.mswindows:
        # POSIX methods

        @check_args
        def _communicate(self: SELF(), endtime: FLOAT | NONE, orig_timeout_seconds: FLOAT):
            if self.__optional_input_stream and not self.__is_communication_started:
                # Flush stdio buffer.  This might block, if the user has
                # been writing to .stdin in an uncontrolled fashion.
                self.__optional_input_stream.flush()

                if not self.__optional_input_data:
                    self.__optional_input_stream.close()

            # Only create this mapping if we haven't already.
            if not self.__is_communication_started:
                for output_stream in self.__optional_output_stream_tuple:
                    self.__output_stream_to_output_dict[output_stream] = []

            # self.__save_input()

            if self.__optional_input_data:
                input_data_view = memoryview(self.__optional_input_data)

            with subprocess._PopenSelector() as selector:

                if self.__optional_input_stream and self.__optional_input_data:
                    selector.register(self.__optional_input_stream, selectors.EVENT_WRITE)

                for output_stream in self.__optional_output_stream_tuple:
                    selector.register(output_stream, selectors.EVENT_READ)

                timeout_seconds = None

                while selector.get_map():
                    if endtime:
                        timeout_seconds = self.__remaining_time(endtime)
                        if timeout_seconds < 0:
                            raise TimeoutExpiredError('Timed out after {} seconds'.format(orig_timeout_seconds))

                    ready_tuple_list = selector.select(timeout_seconds)
                    self.__check_timeout(endtime, orig_timeout_seconds)

                    # XXX Rewrite these to use non-blocking I/O on the file
                    # objects; they are no longer using C stdio!

                    for selector_key, events in ready_tuple_list:

                        if selector_key.fileobj is self.__optional_input_stream:

                            chunk = input_data_view[self.__optional_input_data_offset :
                            self.__optional_input_data_offset + subprocess._PIPE_BUF]
                            try:
                                count = os.write(selector_key.fd, chunk)
                                self.__optional_input_data_offset += count
                            except OSError as e:
                                if e.errno == errno.EPIPE:
                                    selector.unregister(selector_key.fileobj)
                                    selector_key.fileobj.close()
                                else:
                                    raise
                            else:
                                if self.__optional_input_data_offset >= len(self.__optional_input_data):
                                    selector.unregister(selector_key.fileobj)
                                    selector_key.fileobj.close()

                        else:
                            data = os.read(selector_key.fd, 32768)
                            if data:
                                output_list = self.__output_stream_to_output_dict[selector_key.fileobj]
                                output_list.append(data)
                            else:
                                selector.unregister(selector_key.fileobj)
                                selector_key.fileobj.close()

            self.wait(timeout=self.__remaining_time(endtime))

            # All data exchanged.  Translate lists into strings.
            for output_stream in self.__output_stream_to_output_dict:
                output_list = self.__output_stream_to_output_dict[output_stream]
                output_bytes = b''.join(output_list)
                self.__output_stream_to_output_dict[output_stream] = output_bytes

            # Translate newlines, if requested.
            # This also turns bytes into strings.
            if self.universal_newlines:
                if stdout is not None:
                    stdout = self._translate_newlines(stdout,
                                                      self.stdout.encoding)
                if stderr is not None:
                    stderr = self._translate_newlines(stderr,
                                                      self.stderr.encoding)

            return (stdout, stderr)


        def __save_input(self):
            # This method is called from the _communicate_with_*() methods
            # so that if we time out while communicating, we can continue
            # sending input if we retry.
            if self.__optional_input_stream and self._input is None:
                self.__optional_input_data_offset = 0
                self._input = input
                if self.universal_newlines and input is not None:
                    self._input = self._input.encode(self.__optional_input_stream.encoding)


    def __remaining_time(self, endtime):
        """Convenience for _communicate when computing timeouts."""
        if endtime is None:
            return None
        else:
            now = subprocess._time()
            x = endtime - now
            return x


    def __check_timeout(self, endtime, orig_timeout):
        """Convenience for checking if a timeout has expired."""
        if endtime is not None:
            now = subprocess._time()
            if now > endtime:
                raise TimeoutExpiredError(self.args, orig_timeout)


    def communicate(self, input=None, timeout=None):
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.  The optional input argument should be
        bytes to be sent to the child process, or None, if no data
        should be sent to the child.

        communicate() returns a tuple (stdout, stderr)."""

        if self._communication_started and input:
            raise ValueError("Cannot send input after starting communication")

        # Optimization: If we are not worried about timeouts, we haven't
        # started communicating, and we have one or zero pipes, using select()
        # or threads is unnecessary.
        if (timeout is None and not self._communication_started and
                    [self.stdin, self.stdout, self.stderr].count(None) >= 2):
            stdout = None
            stderr = None
            if self.stdin:
                if input:
                    try:
                        self.stdin.write(input)
                    except OSError as e:
                        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                            raise
                self.stdin.close()
            elif self.stdout:
                stdout = _eintr_retry_call(self.stdout.read)
                self.stdout.close()
            elif self.stderr:
                stderr = _eintr_retry_call(self.stderr.read)
                self.stderr.close()
            self.wait()
        else:
            if timeout is not None:
                endtime = _time() + timeout
            else:
                endtime = None

            try:
                stdout, stderr = self._communicate(input, endtime, timeout)
            finally:
                self._communication_started = True

            sts = self.wait(timeout=self.__remaining_time(endtime))

        return (stdout, stderr)



# TODO: Build a tiny path-like env var modifier class.  See old CSharp stuff.
# Can be used for CLASSPATH, PYTHONPATH, PATH and other stuff.


class RSubprocessPipelineBuilder:

    @check_args
    def __init__(self: SELF(),
                 *,
                 args: NON_EMPTY_SEQUENCE_OF(NON_EMPTY_STR),

                 stdin: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                     RSubprocessStreamTypeEnum.PIPE)
                        | INPUT_STREAM
                        | NONE=RSubprocessStreamTypeEnum.DEVNULL,

                 stdout: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                      RSubprocessStreamTypeEnum.PIPE)
                         | OUTPUT_STREAM | NONE=None,

                 stderr: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                      RSubprocessStreamTypeEnum.PIPE,
                                      RSubprocessStreamTypeEnum.STDOUT)
                         | OUTPUT_STREAM | NONE=None,

                 shell: BOOL=False,
                 cwd: NON_EMPTY_STR | NONE=None,
                 env: DICT_OF(key_matcher=NON_EMPTY_STR, value_matcher=STR) | NONE=None,
                 universal_newlines: BOOL=True):

        x = RSubprocessSettings(args=args, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell,
                                cwd=cwd, env=env, universal_newlines=universal_newlines)
        self.__settings_list = [x]

    @check_args
    def append(self: SELF(),
               *,
               args: NON_EMPTY_SEQUENCE_OF(NON_EMPTY_STR),

               stdout: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                    RSubprocessStreamTypeEnum.PIPE)
                       | OUTPUT_STREAM | NONE=None,

               stderr: ANY_VALUE_OF(RSubprocessStreamTypeEnum.DEVNULL,
                                    RSubprocessStreamTypeEnum.PIPE,
                                    RSubprocessStreamTypeEnum.STDOUT)
                       | OUTPUT_STREAM | NONE=None,

               shell: BOOL=False,
               cwd: NON_EMPTY_STR | NONE=None,
               env: DICT_OF(key_matcher=NON_EMPTY_STR, value_matcher=STR) | NONE=None,
               universal_newlines: BOOL=True):

        prev_settings = self.__settings_list[-1]
        prev_settings.stdout = RSubprocessStreamTypeEnum.PIPE

        x = RSubprocessSettings(args=args, stdin=None, stdout=stdout, stderr=stderr, shell=shell,
                                cwd=cwd, env=env, universal_newlines=universal_newlines)
        self.__settings_list.append(x)

    @check_args
    def start(self: SELF()) -> INSTANCE_OF(RSubprocessPipeline):
        x = RSubprocessPipeline(self.__settings_list)
        return x
