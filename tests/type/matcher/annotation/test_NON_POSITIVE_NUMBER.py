from rambutan3.type.matcher.annotation.NON_POSITIVE_NUMBER import NON_POSITIVE_NUMBER


def test():
    assert not NON_POSITIVE_NUMBER.matches("abc")
    assert NON_POSITIVE_NUMBER.matches(-1.234)
    assert NON_POSITIVE_NUMBER.matches(-1)
    assert NON_POSITIVE_NUMBER.matches(0)
    assert NON_POSITIVE_NUMBER.matches(0.0)
    assert not NON_POSITIVE_NUMBER.matches(0.234)
    assert not NON_POSITIVE_NUMBER.matches(1)
    assert not NON_POSITIVE_NUMBER.matches(1.0)
    assert not NON_POSITIVE_NUMBER.matches(1.234)
    assert not NON_POSITIVE_NUMBER.matches(2)
    assert not NON_POSITIVE_NUMBER.matches(2.0)
