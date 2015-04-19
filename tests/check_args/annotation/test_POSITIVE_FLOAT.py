from rambutan3.check_args.annotation.POSITIVE_FLOAT import POSITIVE_FLOAT


def test():
    assert not POSITIVE_FLOAT.matches("abc")
    assert not POSITIVE_FLOAT.matches(-1.234)
    assert not POSITIVE_FLOAT.matches(-1)
    assert not POSITIVE_FLOAT.matches(0)
    assert POSITIVE_FLOAT.matches(0.234)
    assert not POSITIVE_FLOAT.matches(1)
    assert POSITIVE_FLOAT.matches(1.234)
    assert POSITIVE_FLOAT.matches(2.0)
