from rambutan3.type.matcher.annotation.NEGATIVE_FLOAT import NEGATIVE_FLOAT


def test():
    assert not NEGATIVE_FLOAT.matches("abc")
    assert NEGATIVE_FLOAT.matches(-1.234)
    assert not NEGATIVE_FLOAT.matches(-1)
    assert not NEGATIVE_FLOAT.matches(0.0)
    assert not NEGATIVE_FLOAT.matches(0.234)
    assert not NEGATIVE_FLOAT.matches(1.0)
    assert not NEGATIVE_FLOAT.matches(1.234)
    assert not NEGATIVE_FLOAT.matches(2.0)
