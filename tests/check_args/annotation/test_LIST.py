from rambutan3.check_args.annotation.LIST import LIST


def test():
    assert LIST.matches([])
    assert LIST.matches(list())
    assert LIST.matches([1, 2, 3])
    assert LIST.matches([1, 2, 3, "abc"])
    assert LIST.matches([1, 2, 3, "abc", None])
    assert not LIST.matches("abc")
    assert not LIST.matches(None)
    assert not LIST.matches(tuple())
    assert not LIST.matches((1, 2, 3))
