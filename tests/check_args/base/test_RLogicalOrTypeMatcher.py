import pytest

from rambutan3.check_args.base.RAbstractTypeMatcher import RLogicalOrTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher


_INT_MATCHER = RInstanceMatcher(int)
_STR_MATCHER = RInstanceMatcher(str)
_FLOAT_MATCHER = RInstanceMatcher(float)
_BOOL_MATCHER = RInstanceMatcher(bool)


def test_ctor():
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher()
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(None)
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(None, _STR_MATCHER)
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(_INT_MATCHER, None)
    m1 = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    m2 = RLogicalOrTypeMatcher(m1, _FLOAT_MATCHER)
    m3 = RLogicalOrTypeMatcher(_BOOL_MATCHER, m2)
    _assert_ctor(m1, (_INT_MATCHER, _STR_MATCHER))
    _assert_ctor(m2, (_INT_MATCHER, _STR_MATCHER, _FLOAT_MATCHER))
    _assert_ctor(m3, (_BOOL_MATCHER, _INT_MATCHER, _STR_MATCHER, _FLOAT_MATCHER))


def _assert_ctor(logical_or_matcher: RLogicalOrTypeMatcher, expected_matcher_tuple: tuple):
    for actual_matcher, expected_matcher in zip(logical_or_matcher, expected_matcher_tuple):
        assert actual_matcher is expected_matcher


def test_matches():
    matcher = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    assert matcher.matches("abc")
    assert matcher.matches("abc")
    assert matcher.matches(123)
    assert not matcher.matches(None)
    assert not matcher.matches(123.456)


def test__eq__():
    m1 = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    assert not "abc" == m1
    assert not m1 == "abc"
    assert m1 == m1
    m2 = RLogicalOrTypeMatcher(_STR_MATCHER, _INT_MATCHER)
    assert m1 == m2


def test__hash__():
    m1 = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    assert hash(m1) == hash(m1)
    m2 = RLogicalOrTypeMatcher(_STR_MATCHER, _INT_MATCHER)
    assert hash(m1) == hash(m2)


def test__str__():
    assert "int | str" == str(RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER))
    assert "str | int" == str(RLogicalOrTypeMatcher(_STR_MATCHER, _INT_MATCHER))
