import re
from rambutan3.check_args.annotation.STR_MATCHES_REGEX import STR_MATCHES_REGEX


def test():
    assert STR_MATCHES_REGEX(re.compile("^abc"), "starts with 'abc'").matches("abc")
    assert STR_MATCHES_REGEX(re.compile("^abc$"), "exactly 'abc'").matches("abc")
    assert STR_MATCHES_REGEX(re.compile("abc$"), "ends with 'abc'").matches("abc")
    assert STR_MATCHES_REGEX(re.compile("^abc"), "starts with 'abc'").matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("abc"), "contains 'abc'").matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("def"), "contains 'def'").matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("def$"), "ends with 'def'").matches("abcdef")
    assert not STR_MATCHES_REGEX(re.compile("^def"), "starts with 'def'").matches("abcdef")
