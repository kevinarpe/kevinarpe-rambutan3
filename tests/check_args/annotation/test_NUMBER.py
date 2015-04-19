from rambutan3.check_args.annotation.NUMBER import NUMBER


def test():
    assert not NUMBER.matches("abc")
    assert not NUMBER.matches(True)
    assert NUMBER.matches(-1.234)
    assert NUMBER.matches(-1)
    assert NUMBER.matches(0)
    assert NUMBER.matches(0.234)
    assert NUMBER.matches(1)
    assert NUMBER.matches(1.234)
    assert NUMBER.matches(2)
