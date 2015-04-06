from rambutan3.type.matcher.annotation.NUMBER import NUMBER


def test():
    assert not NUMBER.matches("abc")
    assert NUMBER.matches(-1.234)
    assert NUMBER.matches(-1)
    assert NUMBER.matches(0)
    assert NUMBER.matches(0.234)
    assert NUMBER.matches(1)
    assert NUMBER.matches(1.234)
    assert NUMBER.matches(2)
