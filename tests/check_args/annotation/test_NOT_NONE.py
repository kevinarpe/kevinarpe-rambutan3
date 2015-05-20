from rambutan3.check_args.annotation.NOT_NONE import NOT_NONE


def test():
    assert NOT_NONE.matches(123)
    assert NOT_NONE.matches("abc")
    assert NOT_NONE.matches([])
    assert NOT_NONE.matches(dict())
    assert NOT_NONE.matches(set())
    assert NOT_NONE.matches([123])
    assert not NOT_NONE.matches(None)
