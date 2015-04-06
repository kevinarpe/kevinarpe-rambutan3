from rambutan3.type.matcher.annotation.POSITIVE_INT import POSITIVE_INT


def test():
    assert not POSITIVE_INT.matches("abc")
    assert not POSITIVE_INT.matches(-1.234)
    assert not POSITIVE_INT.matches(-1)
    assert not POSITIVE_INT.matches(0)
    assert not POSITIVE_INT.matches(0.234)
    assert POSITIVE_INT.matches(1)
    assert not POSITIVE_INT.matches(1.234)
    assert POSITIVE_INT.matches(2)
