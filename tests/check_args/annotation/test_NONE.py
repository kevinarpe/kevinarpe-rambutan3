from rambutan3.check_args.annotation.NONE import NONE


def test():
    assert not NONE.matches(123)
    assert not NONE.matches("abc")
    assert not NONE.matches([])
    assert not NONE.matches(dict())
    assert not NONE.matches(set())
    assert not NONE.matches([123])
    assert NONE.matches(None)
