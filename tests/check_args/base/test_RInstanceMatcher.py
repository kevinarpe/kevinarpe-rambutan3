import pytest

from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher

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
        RInstanceMatcher("abc")
    with pytest.raises(TypeError):
        RInstanceMatcher(123)
    RInstanceMatcher(int)
    RInstanceMatcher(str)


def test_matches():
    assert RInstanceMatcher(str).matches("abc")
    assert not RInstanceMatcher(str).matches(None)
    assert not RInstanceMatcher(str).matches(123)
    assert RInstanceMatcher(int).matches(123)
    assert not RInstanceMatcher(int).matches(None)
    assert not RInstanceMatcher(int).matches("abc")
    assert RInstanceMatcher(str, int).matches("abc")
    assert RInstanceMatcher(str, int).matches(123)
    assert RInstanceMatcher(int, str).matches("abc")
    assert RInstanceMatcher(int, str).matches(123)


def test__eq__():
    assert not RInstanceMatcher(str) == "abc"
    assert not "abc" == RInstanceMatcher(str)
    assert RInstanceMatcher(str) == RInstanceMatcher(str)
    assert RInstanceMatcher(int, str) == RInstanceMatcher(str, int)


def test__hash__():
    assert hash(RInstanceMatcher(str)) == hash(RInstanceMatcher(str))
    assert hash(RInstanceMatcher(int, str)) == hash(RInstanceMatcher(str, int))


def test__str__():
    assert str(RInstanceMatcher(X)) == X.__name__
    assert str(RInstanceMatcher(X, Y)) == " | ".join((X.__name__, Y.__name__))
