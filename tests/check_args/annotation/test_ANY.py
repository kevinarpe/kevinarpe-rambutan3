from rambutan3.check_args.annotation.ANY import ANY


def test():
    assert ANY.matches(123)
    assert ANY.matches("abc")
    assert ANY.matches([])
    assert ANY.matches(dict())
    assert ANY.matches(set())
    assert ANY.matches([123])
    assert ANY.matches(None)
