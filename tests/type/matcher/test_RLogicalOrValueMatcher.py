import pytest

from rambutan3.type.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.type.matcher.RAbstractTypeMatcher import RLogicalOrTypeMatcher


_INT_MATCHER = RInstanceMatcher(int)
_STR_MATCHER = RInstanceMatcher(str)


def test_ctor():
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher()
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(None)
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(None, _STR_MATCHER)
    with pytest.raises(TypeError):
        RLogicalOrTypeMatcher(_INT_MATCHER, None)
    RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)


def test_matches():
    matcher = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    assert matcher.matches("abc")
    assert matcher.matches("abc")
    assert matcher.matches(123)
    assert not matcher.matches(None)
    assert not matcher.matches(123.456)


def test_iter():
    matcher = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
    it = iter(matcher)
    assert _INT_MATCHER is next(it)
    assert _STR_MATCHER is next(it)
    with pytest.raises(StopIteration):
        next(it)


def test__str__():
    assert "int | str" == str(RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER))
