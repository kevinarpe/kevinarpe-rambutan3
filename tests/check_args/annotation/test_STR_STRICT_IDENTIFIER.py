from rambutan3.check_args.annotation.STR_STRICT_IDENTIFIER import STR_STRICT_IDENTIFIER


def test():
    assert STR_STRICT_IDENTIFIER.matches("abc")
    assert STR_STRICT_IDENTIFIER.matches("_abc")
    assert STR_STRICT_IDENTIFIER.matches("__abc")
    assert not STR_STRICT_IDENTIFIER.matches("0abc")
    assert not STR_STRICT_IDENTIFIER.matches("abc.def")
    assert not STR_STRICT_IDENTIFIER.matches("abc=def")
    assert not STR_STRICT_IDENTIFIER.matches("abc-def")
