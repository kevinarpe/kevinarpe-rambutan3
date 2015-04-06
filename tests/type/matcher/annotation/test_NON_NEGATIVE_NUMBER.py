from rambutan3.type.matcher.annotation.NON_NEGATIVE_NUMBER import NON_NEGATIVE_NUMBER


def test():
    assert not NON_NEGATIVE_NUMBER.matches("abc")
    assert not NON_NEGATIVE_NUMBER.matches(-1.234)
    assert not NON_NEGATIVE_NUMBER.matches(-1)
    assert NON_NEGATIVE_NUMBER.matches(0)
    assert NON_NEGATIVE_NUMBER.matches(0.0)
    assert NON_NEGATIVE_NUMBER.matches(0.234)
    assert NON_NEGATIVE_NUMBER.matches(1)
    assert NON_NEGATIVE_NUMBER.matches(1.0)
    assert NON_NEGATIVE_NUMBER.matches(1.234)
    assert NON_NEGATIVE_NUMBER.matches(2)
    assert NON_NEGATIVE_NUMBER.matches(2.0)
