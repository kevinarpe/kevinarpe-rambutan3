from rambutan3.check_args.annotation.ITERABLE import ITERABLE


def test():
    assert ITERABLE.matches([])
    assert ITERABLE.matches(list())
    assert ITERABLE.matches([1, 2, 3])
    assert ITERABLE.matches([1, 2, 3, "abc"])
    assert ITERABLE.matches([1, 2, 3, "abc", None])
    assert not ITERABLE.matches("abc")
    assert not ITERABLE.matches(None)
    assert ITERABLE.matches(tuple())
    assert ITERABLE.matches((1, 2, 3))
