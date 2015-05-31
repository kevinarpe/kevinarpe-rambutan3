import os
import tempfile
import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.file.RFilePathMatcher import RFilePathMatcher
from rambutan3.op_sys.RFileAccessEnum import RFileAccessEnum
from rambutan3.op_sys.RFileTypeEnum import RFileTypeEnum


def test_ctor():
    with pytest.raises(TypeError):
        RFilePathMatcher()

    with pytest.raises(TypeError):
        RFilePathMatcher('abc', 'def')

    RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ)
    RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ, RFileAccessEnum.WRITE)
    RFilePathMatcher(RFileTypeEnum.REGULAR_FILE, RFileAccessEnum.READ, RFileAccessEnum.WRITE, RFileAccessEnum.EXECUTE)


def test_check_arg():
    # Does not exist
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], 'abc', is_ok=False)

    # Path is not a 'str'
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], 123, is_ok=False)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], None, is_ok=False)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], [None], is_ok=False)

    temp_file = tempfile.NamedTemporaryFile()

    os.chmod(temp_file.name, 0o644)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], temp_file.name, is_ok=True)
    __check_arg(RFileTypeEnum.DIRECTORY, [RFileAccessEnum.READ], temp_file.name, is_ok=False)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ, RFileAccessEnum.WRITE], temp_file.name, is_ok=True)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ, RFileAccessEnum.EXECUTE], temp_file.name, is_ok=False)

    os.chmod(temp_file.name, 0o755)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ, RFileAccessEnum.EXECUTE], temp_file.name, is_ok=True)

    os.chmod(temp_file.name, 0o000)
    for fa in RFileAccessEnum:
        __check_arg(RFileTypeEnum.REGULAR_FILE, [fa], temp_file.name, is_ok=False)
        __check_arg(RFileTypeEnum.DIRECTORY, [fa], temp_file.name, is_ok=False)

    # Allow clean-up
    os.chmod(temp_file.name, 0o644)

    temp_dir = tempfile.TemporaryDirectory()

    os.chmod(temp_dir.name, 0o755)
    __check_arg(RFileTypeEnum.DIRECTORY, [RFileAccessEnum.READ], temp_dir.name, is_ok=True)
    __check_arg(RFileTypeEnum.REGULAR_FILE, [RFileAccessEnum.READ], temp_dir.name, is_ok=False)
    __check_arg(RFileTypeEnum.DIRECTORY, [RFileAccessEnum.READ, RFileAccessEnum.WRITE], temp_dir.name, is_ok=True)
    __check_arg(RFileTypeEnum.DIRECTORY, [RFileAccessEnum.READ, RFileAccessEnum.EXECUTE], temp_dir.name, is_ok=True)

    os.chmod(temp_dir.name, 0o644)
    __check_arg(RFileTypeEnum.DIRECTORY, [RFileAccessEnum.READ, RFileAccessEnum.EXECUTE], temp_dir.name, is_ok=False)

    os.chmod(temp_dir.name, 0o000)
    for fa in RFileAccessEnum:
        __check_arg(RFileTypeEnum.REGULAR_FILE, [fa], temp_dir.name, is_ok=False)
        __check_arg(RFileTypeEnum.DIRECTORY, [fa], temp_dir.name, is_ok=False)

    # Allow clean-up
    os.chmod(temp_dir.name, 0o755)


def __check_arg(file_type: RFileTypeEnum, file_access_iterable, path: str, *, is_ok: bool):
    m = RFilePathMatcher(file_type, *file_access_iterable)
    if is_ok:
        assert m.check_arg(path, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(path, 'dummy_arg_name')


def test__eq__and__ne__and__hash__():
    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             'abc',
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             is_equal=True)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             RFilePathMatcher(RFileTypeEnum.REGULAR_FILE, RFileAccessEnum.READ),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.WRITE),
                             RFilePathMatcher(RFileTypeEnum.REGULAR_FILE, RFileAccessEnum.READ),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.WRITE),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.WRITE, RFileAccessEnum.READ),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ),
                             RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ, RFileAccessEnum.WRITE),
                             is_equal=False)


def test__str__():
    assert str(RFilePathMatcher(RFileTypeEnum.NAMED_PIPE, RFileAccessEnum.READ)) \
           == 'path to file of type NAMED_PIPE with modes: READ'
