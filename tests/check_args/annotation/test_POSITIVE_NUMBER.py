from rambutan3.check_args.annotation.POSITIVE_NUMBER import POSITIVE_NUMBER


def test():
    assert not POSITIVE_NUMBER.matches("abc")
    assert not POSITIVE_NUMBER.matches(-1.234)
    assert not POSITIVE_NUMBER.matches(-1)
    assert not POSITIVE_NUMBER.matches(0)
    assert not POSITIVE_NUMBER.matches(0.0)
    assert not POSITIVE_NUMBER.matches(True)
    assert POSITIVE_NUMBER.matches(0.234)
    assert POSITIVE_NUMBER.matches(1)
    assert POSITIVE_NUMBER.matches(1.0)
    assert POSITIVE_NUMBER.matches(1.234)
    assert POSITIVE_NUMBER.matches(2)
    assert POSITIVE_NUMBER.matches(2.0)
