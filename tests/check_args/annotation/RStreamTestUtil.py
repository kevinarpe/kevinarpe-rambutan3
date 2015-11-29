import subprocess
from collections import namedtuple
from subprocess import Popen


RStreamTestUtilTuple = namedtuple('RStreamTestUtilTuple',
                                  [
                                      'buffered_writer',
                                      'buffered_reader',
                                      'writable_text_io_wrapper',
                                      'readable_text_io_wrapper'
                                  ])


def create_stream_test_tuple():
    p = __popen(universal_newlines=False)
    buffered_writer = p.stdin
    buffered_reader = p.stdout

    p2 = __popen(universal_newlines=True)
    writable_text_io_wrapper = p2.stdin
    readable_text_io_wrapper = p2.stdout

    x = RStreamTestUtilTuple(buffered_writer, buffered_reader, writable_text_io_wrapper, readable_text_io_wrapper)
    return x


def __popen(*, universal_newlines: bool):
    # This command should be cross-platform for Windows, Unix, and MacOS X
    p = Popen(args=['echo', 'abc'],
              stdin=subprocess.PIPE,
              stdout=subprocess.PIPE,
              universal_newlines=universal_newlines,
              shell=True)
    # p.communicate()
    return p
    # stdin
    #   universal_newlines=False
    #       (<class '_io.BufferedWriter'>, <class '_io._BufferedIOBase'>, <class '_io._IOBase'>, <class 'object'>)
    #   universal_newlines=True
    #       (<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)
    # stdout
    #   universal_newlines=False
    #       (<class '_io.BufferedReader'>, <class '_io._BufferedIOBase'>, <class '_io._IOBase'>, <class 'object'>)
    #   universal_newlines=True
    #       (<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)
