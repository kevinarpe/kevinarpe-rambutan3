from rambutan3.check_args.annotation.STR_IDENTIFIER import STR_IDENTIFIER


def test():
    assert STR_IDENTIFIER.matches("abc")
    assert STR_IDENTIFIER.matches("_abc")
    assert STR_IDENTIFIER.matches("__abc")
    assert not STR_IDENTIFIER.matches("0abc")
    assert not STR_IDENTIFIER.matches("abc.def")
