from rambutan3.check_args.annotation.NON_EMPTY_STR import NON_EMPTY_STR
from rambutan3.string.RNonEmptyStr import RNonEmptyStr


def test():
    assert not NON_EMPTY_STR.matches(123)
    assert NON_EMPTY_STR.matches("abc")
    assert NON_EMPTY_STR.matches(RNonEmptyStr("abc"))
    assert not NON_EMPTY_STR.matches("")
    assert not NON_EMPTY_STR.matches(None)
