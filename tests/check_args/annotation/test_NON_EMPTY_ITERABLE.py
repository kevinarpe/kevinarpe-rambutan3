from rambutan3.check_args.annotation.NON_EMPTY_ITERABLE import NON_EMPTY_ITERABLE


def test():
    assert NON_EMPTY_ITERABLE.matches([123])
    assert not NON_EMPTY_ITERABLE.matches([])
    assert not NON_EMPTY_ITERABLE.matches(list())
    assert NON_EMPTY_ITERABLE.matches(["abc"])
    assert NON_EMPTY_ITERABLE.matches(["abc", 123])
    assert NON_EMPTY_ITERABLE.matches(["abc", 123, None])
    assert not NON_EMPTY_ITERABLE.matches(None)
    assert not NON_EMPTY_ITERABLE.matches(123)
    assert not NON_EMPTY_ITERABLE.matches(True)
    assert not NON_EMPTY_ITERABLE.matches({})
    assert NON_EMPTY_ITERABLE.matches({123: "abc"})
