from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT


def test():
    assert not NON_NEGATIVE_INT.matches("abc")
    assert not NON_NEGATIVE_INT.matches(-1.234)
    assert not NON_NEGATIVE_INT.matches(-1)
    assert NON_NEGATIVE_INT.matches(0)
    assert not NON_NEGATIVE_INT.matches(0.234)
    assert NON_NEGATIVE_INT.matches(1)
    assert not NON_NEGATIVE_INT.matches(1.234)
    assert NON_NEGATIVE_INT.matches(2)
