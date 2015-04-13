from rambutan3.type.matcher.annotation.NON_EMPTY_LIST import NON_EMPTY_LIST


def test():
    assert NON_EMPTY_LIST.matches([123])
    assert not NON_EMPTY_LIST.matches([])
    assert not NON_EMPTY_LIST.matches(list())
    assert NON_EMPTY_LIST.matches(["abc"])
    assert NON_EMPTY_LIST.matches(["abc", 123])
    assert NON_EMPTY_LIST.matches(["abc", 123, None])
    assert not NON_EMPTY_LIST.matches(None)
    assert not NON_EMPTY_LIST.matches(123)
    assert not NON_EMPTY_LIST.matches(True)
    assert not NON_EMPTY_LIST.matches({})
    assert not NON_EMPTY_LIST.matches({123: "abc"})
