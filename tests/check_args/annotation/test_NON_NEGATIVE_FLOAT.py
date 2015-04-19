from rambutan3.check_args.annotation.NON_NEGATIVE_FLOAT import NON_NEGATIVE_FLOAT


def test():
    assert not NON_NEGATIVE_FLOAT.matches("abc")
    assert not NON_NEGATIVE_FLOAT.matches(-1.234)
    assert not NON_NEGATIVE_FLOAT.matches(-1)
    assert NON_NEGATIVE_FLOAT.matches(0.0)
    assert NON_NEGATIVE_FLOAT.matches(0.234)
    assert not NON_NEGATIVE_FLOAT.matches(1)
    assert NON_NEGATIVE_FLOAT.matches(1.234)
    assert not NON_NEGATIVE_FLOAT.matches(2)
