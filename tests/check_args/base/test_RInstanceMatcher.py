import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher

from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher


class X:
    pass


class Y:
    pass


def test_ctor():
    with pytest.raises(ValueError):
        RInstanceMatcher()

    with pytest.raises(TypeError):
        RInstanceMatcher(None)

    with pytest.raises(TypeError):
        RInstanceMatcher('abc')

    with pytest.raises(TypeError):
        RInstanceMatcher(123)

    RInstanceMatcher(int)
    RInstanceMatcher(str)


def test_check_arg():
    __check_arg((str,), 'abc', 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((str,), None, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((str,), 123, 'dummy_arg_name')

    __check_arg((int,), 123, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((int,), None, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((int,), 'abc', 'dummy_arg_name')

    __check_arg((str, int), 'abc', 'dummy_arg_name')
    __check_arg((str, int), 123, 'dummy_arg_name')
    __check_arg((int, str), 'abc', 'dummy_arg_name')
    __check_arg((int, str), 123, 'dummy_arg_name')


def __check_arg(class_or_type_tuple, value, arg_name: str, *arg_name_format_args):
    m = RInstanceMatcher(*class_or_type_tuple)
    assert value is m.check_arg(value, arg_name, *arg_name_format_args)


def test__or__():
    __or((str, ), INT, 'abc', 'dummy_arg_name', is_exception_expected=False)
    __or((str, ), INT, 123, 'dummy_arg_name', is_exception_expected=False)
    __or((str, ), INT, 123.456, 'dummy_arg_name', is_exception_expected=True)


def __or(class_or_type_tuple,
         other_matcher: RAbstractTypeMatcher,
         value,
         arg_name: str,
         *,
         is_exception_expected: bool):

    m = RInstanceMatcher(*class_or_type_tuple)

    m2 = m | other_matcher

    if is_exception_expected:
        with pytest.raises(RCheckArgsError):
            assert value is m2.check_arg(value, arg_name)
    else:
        assert value is m2.check_arg(value, arg_name)

    m3 = other_matcher | m

    if is_exception_expected:
        with pytest.raises(RCheckArgsError):
            assert value is m3.check_arg(value, arg_name)
    else:
        assert value is m3.check_arg(value, arg_name)


def test__eq__and__ne__():
    RTestUtil.test_eq_ne_hash(RInstanceMatcher(str), 'abc', is_equal=False)
    RTestUtil.test_eq_ne_hash('abc', RInstanceMatcher(str), is_equal=False)
    RTestUtil.test_eq_ne_hash(RInstanceMatcher(str), RInstanceMatcher(str), is_equal=True)
    RTestUtil.test_eq_ne_hash(RInstanceMatcher(int, str), RInstanceMatcher(str, int), is_equal=True)


def test__hash__():
    assert hash(RInstanceMatcher(str)) == hash(RInstanceMatcher(str))
    assert hash(RInstanceMatcher(str)) != hash(RInstanceMatcher(int))
    assert hash(RInstanceMatcher(int, str)) == hash(RInstanceMatcher(str, int))
    assert hash(RInstanceMatcher(int, str)) != hash(RInstanceMatcher(str))
    assert hash(RInstanceMatcher(int, str)) != hash(RInstanceMatcher(int))


def test__str__():
    assert str(RInstanceMatcher(X)) == X.__name__
    assert str(RInstanceMatcher(X, Y)) == ' | '.join((X.__name__, Y.__name__))
