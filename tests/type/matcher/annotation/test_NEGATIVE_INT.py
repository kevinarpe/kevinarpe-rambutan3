from rambutan3.type.matcher.annotation.NEGATIVE_INT import NEGATIVE_INT


def test():
    assert not NEGATIVE_INT.matches("abc")
    assert not NEGATIVE_INT.matches(-1.234)
    assert NEGATIVE_INT.matches(-1)
    assert not NEGATIVE_INT.matches(0)
    assert not NEGATIVE_INT.matches(0.234)
    assert not NEGATIVE_INT.matches(1)
    assert not NEGATIVE_INT.matches(1.234)
    assert not NEGATIVE_INT.matches(2)
