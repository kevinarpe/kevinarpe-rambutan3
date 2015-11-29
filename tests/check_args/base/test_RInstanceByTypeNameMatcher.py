import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.base.RInstanceByTypeNameMatcher import RInstanceByTypeNameMatcher


class XYZ:
    pass


class XYZ2:
    pass


def test_ctor():
    with pytest.raises(TypeError):
        RInstanceByTypeNameMatcher()

    with pytest.raises(TypeError):
        RInstanceByTypeNameMatcher(123)

    with pytest.raises(ValueError):
        RInstanceByTypeNameMatcher('123')

    RInstanceByTypeNameMatcher('abc')


def test_check_arg():
    __check_arg('XYZ', XYZ(), is_ok=True)
    __check_arg(XYZ.__name__, XYZ(), is_ok=True)
    __check_arg(XYZ.__name__, 'abc', is_ok=False)
    __check_arg(XYZ.__name__, 123.456, is_ok=False)
    __check_arg('abc' + XYZ.__name__, XYZ(), is_ok=False)
    __check_arg(XYZ.__name__, XYZ2(), is_ok=False)
    __check_arg(XYZ2.__name__, XYZ(), is_ok=False)


def __check_arg(type_name: str, value, *, is_ok: bool):
    m = RInstanceByTypeNameMatcher(type_name)
    if is_ok:
        assert m.check_arg(value, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(value, 'dummy_arg_name')


def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(RInstanceByTypeNameMatcher('XYZ'), 'abc', is_equal=False)
    RTestUtil.test_eq_ne_hash(RInstanceByTypeNameMatcher('XYZ'), RInstanceByTypeNameMatcher('XYZ'), is_equal=True)


def test__str__():
    assert str(RInstanceByTypeNameMatcher('XYZ')) == 'XYZ'
    assert str(RInstanceByTypeNameMatcher(XYZ.__name__)) == XYZ.__name__
