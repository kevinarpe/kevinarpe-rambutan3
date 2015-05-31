import pytest
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.other.RRangeSizeStr import RRangeSizeStr
from tests.check_args.collection import test_RRangeSizeMatcher


def test_ctor():
    test_RRangeSizeMatcher.core_test_ctor(RRangeSizeStr)


def test_check_arg():
    with pytest.raises(RCheckArgsError):
        __check_arg([123], min_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg([123], max_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg([123], min_size=1, max_size=2)

    with pytest.raises(RCheckArgsError):
        __check_arg(None, min_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg(123, min_size=1)

    __check_arg('abc', min_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg('abc', min_size=4)

    __check_arg('abc', max_size=3)

    with pytest.raises(RCheckArgsError):
        __check_arg('abc', max_size=2)

    with pytest.raises(RCheckArgsError):
        __check_arg('', min_size=1, max_size=3)

    __check_arg('a', min_size=1, max_size=3)
    __check_arg('ab', min_size=1, max_size=3)
    __check_arg('abc', min_size=1, max_size=3)

    with pytest.raises(RCheckArgsError):
        __check_arg('abcd', min_size=1, max_size=3)


def __check_arg(value, *, min_size: int=-1, max_size: int=-1):
    m = RRangeSizeStr(min_size=min_size, max_size=max_size)
    assert value is m.check_arg(value, 'dummy_arg_name')


def test__eq__and__ne__():
    test_RRangeSizeMatcher.core_test__eq__and__ne__(RRangeSizeStr)


def test__hash__():
    test_RRangeSizeMatcher.core_test__hash__(RRangeSizeStr)


def test__str__():
    assert str(RRangeSizeStr(min_size=1)) == 'str where size >= 1'
    assert str(RRangeSizeStr(max_size=1)) == 'str where size <= 1'
    assert str(RRangeSizeStr(min_size=1, max_size=2)) == 'str where size >= 1 and size <= 2'
