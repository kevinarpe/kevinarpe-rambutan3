import pytest
import types

from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.base.RInstanceWithPredicateMatcher import RInstanceWithPredicateMatcher
from rambutan3.string.RMessageText import RMessageText


def test_ctor():
    with pytest.raises(TypeError):
        RInstanceWithPredicateMatcher()

    with pytest.raises(TypeError):
        RInstanceWithPredicateMatcher(123, RMessageText('len >= 3'), str)

    with pytest.raises(TypeError):
        RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, 123, str)

    with pytest.raises(TypeError):
        RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, RMessageText('len >= 3'), 123)

    RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, RMessageText('len >= 3'), str)


def test_check_arg():
    __check_arg(lambda x: len(x) >= 3, 'len >= 3', (str,), 'abc', is_ok=True)
    # Predicate result is not boolean
    __check_arg(lambda x: 'abc', 'len >= 3', (str,), 'abc', is_ok=False)
    # TypeError: int value 123 is not type str
    __check_arg(lambda x: len(x) >= 3, 'len >= 3', (str,), 123, is_ok=False)
    # int value 123 has correct type, but predicate throws exception
    __check_arg(lambda x: len(x) >= 3, 'len >= 3', (str, int), 123, is_ok=False)
    # Predicate failure: String is too short
    __check_arg(lambda x: len(x) >= 3, 'len >= 3', (str,), 'ab', is_ok=False)


def __check_arg(predicate_func: types.FunctionType,
                predicate_description: str,
                class_or_type_tuple,
                value,
                *,
                is_ok: bool):
    m = RInstanceWithPredicateMatcher(predicate_func, RMessageText(predicate_description), *class_or_type_tuple)
    if is_ok:
        assert m.check_arg(value, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(value, 'dummy_arg_name')


def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(
        RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, RMessageText('len >= 3'), str),
        'abc',
        is_equal=False)

    # Comparing function references is by (internal) object ID.
    # Thus we need to use exactly the same lambda ref, not just an equivalent one.
    lambda_ref = lambda x: len(x) >= 3
    RTestUtil.test_eq_ne_hash(
        RInstanceWithPredicateMatcher(lambda_ref, RMessageText('len >= 3'), str),
        RInstanceWithPredicateMatcher(lambda_ref, RMessageText('len >= 3'), str),
        is_equal=True)

    # Not equal because the two lambda refs are not equal (==).
    RTestUtil.test_eq_ne_hash(
        RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, RMessageText('len >= 3'), str),
        RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, RMessageText('len >= 3'), str),
        is_equal=False)


def test__str__():
    predicate_description = RMessageText('len >= 3')
    class_or_type = str
    assert str(RInstanceWithPredicateMatcher(lambda x: len(x) >= 3, predicate_description, class_or_type)) \
           == \
           "{} with predicate: '{}'".format(class_or_type.__name__, predicate_description)
