import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher

from rambutan3.check_args.base.RLogicalNotTypeMatcher import RLogicalNotTypeMatcher


def test_ctor():
    with pytest.raises(TypeError):
        RLogicalNotTypeMatcher()

    with pytest.raises(TypeError):
        RLogicalNotTypeMatcher(123)

    with pytest.raises(TypeError):
        RLogicalNotTypeMatcher('abc')

    RLogicalNotTypeMatcher(INT)


def test_check_arg():
    __check_arg(INT, 'abc', is_ok=True)
    __check_arg(INT, 123, is_ok=False)
    __check_arg(INT, True, is_ok=True)
    __check_arg(INT, 123.456, is_ok=True)
    __check_arg(INT, [123], is_ok=True)


def __check_arg(delegate: RAbstractTypeMatcher, value, *, is_ok: bool):
    m = RLogicalNotTypeMatcher(delegate)
    if is_ok:
        assert m.check_arg(value, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(value, 'dummy_arg_name')


def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(RLogicalNotTypeMatcher(INT), 'abc', is_equal=False)
    RTestUtil.test_eq_ne_hash(RLogicalNotTypeMatcher(INT), RLogicalNotTypeMatcher(INT), is_equal=True)
    RTestUtil.test_eq_ne_hash(RLogicalNotTypeMatcher(INT | STR), RLogicalNotTypeMatcher(INT | STR), is_equal=True)
    RTestUtil.test_eq_ne_hash(RLogicalNotTypeMatcher(INT | STR), RLogicalNotTypeMatcher(STR | INT), is_equal=True)


def test__str__():
    assert str(RLogicalNotTypeMatcher(INT)) == 'not int'
