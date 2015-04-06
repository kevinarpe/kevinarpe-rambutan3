from rambutan3.type.matcher.annotation.INT import INT


def test():
    assert not INT.matches("abc")
    assert not INT.matches(-1.234)
    assert INT.matches(-1)
    assert INT.matches(0)
    assert not INT.matches(0.234)
    assert INT.matches(1)
    assert not INT.matches(1.234)
    assert INT.matches(2)
