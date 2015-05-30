import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.base.RAnyValueOfMatcher import RAnyValueOfMatcher


def test_ctor():
    with pytest.raises(ValueError):
        RAnyValueOfMatcher()


def test_check_arg():
    __check_arg((123,), 123, 'dummy_arg_name')
    __check_arg((123, 'abc'), 123, 'dummy_arg_name')
    __check_arg((123, 'abc'), 'abc', 'dummy_arg_name')
    __check_arg((123, 456, 789), 123, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((123, 456, 789), 'abc', 'dummy_arg_name')

    __check_arg((123, 456, 'abc', 789), 'abc', 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((123, 'ABC'), 'abc', 'dummy_arg_name')

    __check_arg((str,), str, 'dummy_arg_name')

    with pytest.raises(RCheckArgsError):
        __check_arg((str,), int, 'dummy_arg_name')

    __check_arg((str, int), str, 'dummy_arg_name')
    __check_arg((str, int), int, 'dummy_arg_name')


def __check_arg(value_tuple, value, arg_name: str, *arg_name_format_args):
    m = RAnyValueOfMatcher(*value_tuple)
    assert value is m.check_arg(value, arg_name, *arg_name_format_args)


def test__eq__and__ne__():
    RTestUtil.test_eq_and_ne(RAnyValueOfMatcher(str), 'abc', is_equal=False)
    RTestUtil.test_eq_and_ne('abc', RAnyValueOfMatcher(str), is_equal=False)
    RTestUtil.test_eq_and_ne(RAnyValueOfMatcher(str), RAnyValueOfMatcher(str), is_equal=True)
    RTestUtil.test_eq_and_ne(RAnyValueOfMatcher(int, str), RAnyValueOfMatcher(str, int), is_equal=True)


def test__hash__():
    assert hash(RAnyValueOfMatcher(str)) == hash(RAnyValueOfMatcher(str))
    assert hash(RAnyValueOfMatcher(int, str)) == hash(RAnyValueOfMatcher(str, int))


def test__str__():
    assert str(RAnyValueOfMatcher(123, 'abc')) == 'any value of {}'.format(frozenset((123, 'abc')))
