import pytest

from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.binary_seq.RBinarySequenceEnum import RBinarySequenceEnum
from rambutan3.check_args.binary_seq.RBinarySequenceMatcher import RBinarySequenceMatcher


def test_ctor():
    with pytest.raises(TypeError):
        RBinarySequenceMatcher()

    with pytest.raises(TypeError):
        RBinarySequenceMatcher(None)

    with pytest.raises(TypeError):
        RBinarySequenceMatcher('abc')

    with pytest.raises(TypeError):
        RBinarySequenceMatcher(123)

    RBinarySequenceMatcher(RBinarySequenceEnum.BYTES)


def test_check_arg():
    __check_arg(RBinarySequenceEnum.BYTES, bytes(), 'dummy_arg_name')

    __check_arg(RBinarySequenceEnum.BYTES, b'', 'dummy_arg_name')

    __check_arg(RBinarySequenceEnum.BYTES, b'abc', 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg(RBinarySequenceEnum.BYTES, None, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg(RBinarySequenceEnum.BYTES, 123, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg(RBinarySequenceEnum.BYTES, bytearray(), 'dummy_arg_name')

    __check_arg(RBinarySequenceEnum.BYTEARRAY, bytearray(), 'dummy_arg_name')
    __check_arg(RBinarySequenceEnum.MEMORYVIEW, memoryview(b'abc'), 'dummy_arg_name')
    __check_arg(RBinarySequenceEnum.BINARY_SEQUENCE, bytearray(), 'dummy_arg_name')


def __check_arg(binary_seq_enum: RBinarySequenceEnum, value, arg_name: str, *arg_name_format_args):
    m = RBinarySequenceMatcher(binary_seq_enum)
    assert value is m.check_arg(value, arg_name, *arg_name_format_args)


def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(
        RBinarySequenceMatcher(RBinarySequenceEnum.MEMORYVIEW),
        'abc',
        is_equal=False)

    RTestUtil.test_eq_ne_hash(
        RBinarySequenceMatcher(RBinarySequenceEnum.MEMORYVIEW),
        RBinarySequenceMatcher(RBinarySequenceEnum.MEMORYVIEW),
        is_equal=True)


def test__str__():
    assert str(RBinarySequenceMatcher(RBinarySequenceEnum.BYTES)) == 'bytes'
    assert str(RBinarySequenceMatcher(RBinarySequenceEnum.BYTES)) == RBinarySequenceEnum.BYTES.value[0].__name__
