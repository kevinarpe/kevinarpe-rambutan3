from rambutan3.type.matcher.annotation.FLOAT import FLOAT


def test():
    assert not FLOAT.matches("abc")
    assert FLOAT.matches(-1.234)
    assert not FLOAT.matches(-1)
    assert not FLOAT.matches(0)
    assert FLOAT.matches(0.234)
    assert not FLOAT.matches(1)
    assert FLOAT.matches(1.234)
    assert not FLOAT.matches(2)
