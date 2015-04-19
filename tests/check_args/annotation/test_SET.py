from rambutan3.check_args.annotation.SET import SET


def test():
    assert SET.matches(set())
    assert SET.matches({1, 2, 3})
    assert SET.matches({1, 2, 3, "abc"})
    assert SET.matches({1, 2, 3, "abc", None})
    assert not SET.matches("abc")
    assert not SET.matches(None)
    assert not SET.matches(tuple())
    assert not SET.matches((1, 2, 3))
