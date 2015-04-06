from rambutan3.type.matcher.annotation.NEGATIVE_NUMBER import NEGATIVE_NUMBER


def test():
    assert not NEGATIVE_NUMBER.matches("abc")
    assert NEGATIVE_NUMBER.matches(-1.234)
    assert NEGATIVE_NUMBER.matches(-1)
    assert not NEGATIVE_NUMBER.matches(0)
    assert not NEGATIVE_NUMBER.matches(0.0)
    assert not NEGATIVE_NUMBER.matches(0.234)
    assert not NEGATIVE_NUMBER.matches(1)
    assert not NEGATIVE_NUMBER.matches(1.0)
    assert not NEGATIVE_NUMBER.matches(1.234)
    assert not NEGATIVE_NUMBER.matches(2)
    assert not NEGATIVE_NUMBER.matches(2.0)
