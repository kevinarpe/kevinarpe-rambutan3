from rambutan3.type.matcher.annotation.NON_POSITIVE_FLOAT import NON_POSITIVE_FLOAT


def test():
    assert not NON_POSITIVE_FLOAT.matches("abc")
    assert NON_POSITIVE_FLOAT.matches(-1.234)
    assert not NON_POSITIVE_FLOAT.matches(-1)
    assert not NON_POSITIVE_FLOAT.matches(0)
    assert NON_POSITIVE_FLOAT.matches(0.0)
    assert not NON_POSITIVE_FLOAT.matches(0.234)
    assert not NON_POSITIVE_FLOAT.matches(1)
    assert not NON_POSITIVE_FLOAT.matches(1.234)
    assert not NON_POSITIVE_FLOAT.matches(2)
