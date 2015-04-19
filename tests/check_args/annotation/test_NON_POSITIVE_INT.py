from rambutan3.check_args.annotation.NON_POSITIVE_INT import NON_POSITIVE_INT


def test():
    assert not NON_POSITIVE_INT.matches("abc")
    assert not NON_POSITIVE_INT.matches(-1.234)
    assert NON_POSITIVE_INT.matches(-1)
    assert NON_POSITIVE_INT.matches(0)
    assert not NON_POSITIVE_INT.matches(0.234)
    assert not NON_POSITIVE_INT.matches(1)
    assert not NON_POSITIVE_INT.matches(1.234)
    assert not NON_POSITIVE_INT.matches(2)
