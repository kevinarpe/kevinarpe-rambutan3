import types

from rambutan3.check_args.annotation.BUILTIN_FROZENSET_OF import BUILTIN_FROZENSET_OF
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.annotation.TUPLE import TUPLE
from rambutan3.check_args.annotation.TUPLE_OF import TUPLE_OF
from rambutan3.check_args.set.RSetMatcher import RSetMatcher


def core_test_set_matcher(set_matcher: RSetMatcher, set_ctor: types.FunctionType):
    assert set_matcher.matches(set_ctor())
    assert set_matcher.matches(set_ctor((1, 2, 3)))
    assert set_matcher.matches(set_ctor((1, 2, 3, "abc")))
    assert set_matcher.matches(set_ctor((1, 2, 3, "abc", None)))
    assert not set_matcher.matches("abc")
    assert not set_matcher.matches(None)
    assert not set_matcher.matches(tuple())
    assert not set_matcher.matches((1, 2, 3))


def core_test_set_of_matcher(set_of_matcher: types.FunctionType):
    assert set_of_matcher(INT).matches(set())
    assert set_of_matcher(TUPLE).matches({(1, 2), (3, 4)})
    assert set_of_matcher(TUPLE_OF(STR)).matches({("a", "b"), ("d", "e")})
    assert set_of_matcher(INT).matches({1, 2, 3})
    assert not set_of_matcher(INT).matches({1, 2, 3, "abc"})
    assert set_of_matcher(INT | STR).matches({1, 2, 3, "abc"})
    assert not set_of_matcher(INT).matches({1, 2, 3, "abc", None})
    assert set_of_matcher(INT | STR | NONE).matches({1, 2, 3, "abc", None})
    assert not set_of_matcher(INT).matches("abc")
    assert not set_of_matcher(INT).matches(None)
    assert not set_of_matcher(INT).matches(tuple())
    assert not set_of_matcher(INT).matches((1, 2, 3))


def core_test_non_empty_set_matcher(non_empty_set_matcher: RSetMatcher, set_ctor: types.FunctionType):
    assert non_empty_set_matcher.matches(set_ctor((123,)))
    assert not non_empty_set_matcher.matches(set_ctor())
    assert non_empty_set_matcher.matches(set_ctor(("abc",)))
    assert non_empty_set_matcher.matches(set_ctor(("abc", 123,)))
    assert non_empty_set_matcher.matches(set_ctor(("abc", 123, None,)))
    assert not non_empty_set_matcher.matches(None)
    assert not non_empty_set_matcher.matches(123)
    assert not non_empty_set_matcher.matches(True)
    assert not non_empty_set_matcher.matches({})
    assert not non_empty_set_matcher.matches({123: "abc"})


def core_test_non_empty_set_of_matcher(non_empty_set_of_matcher: types.FunctionType, set_ctor: types.FunctionType):
    assert not non_empty_set_of_matcher(INT).matches(set_ctor())
    assert non_empty_set_of_matcher(TUPLE).matches(set_ctor(((1, 2), (3, 4), tuple())))
    assert non_empty_set_of_matcher(BUILTIN_FROZENSET_OF(STR)).matches(set_ctor((frozenset(("a", "b")), frozenset(("d", "e")))))
    assert not non_empty_set_of_matcher(INT).matches(set_ctor())
    assert non_empty_set_of_matcher(INT).matches(set_ctor((1, 2, 3)))
    assert not non_empty_set_of_matcher(INT).matches(set_ctor((1, 2, 3, "abc")))
    assert non_empty_set_of_matcher(INT | STR).matches(set_ctor((1, 2, 3, "abc")))
    assert not non_empty_set_of_matcher(INT).matches(set_ctor((1, 2, 3, "abc", None)))
    assert non_empty_set_of_matcher(INT | STR | NONE).matches(set_ctor((1, 2, 3, "abc", None)))
    assert not non_empty_set_of_matcher(INT).matches("abc")
    assert not non_empty_set_of_matcher(INT).matches(None)
    assert not non_empty_set_of_matcher(INT).matches(tuple())
    assert not non_empty_set_of_matcher(INT).matches((1, 2, 3))
