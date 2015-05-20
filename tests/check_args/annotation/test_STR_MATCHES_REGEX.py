import re
from rambutan3.check_args.annotation.STR_MATCHES_REGEX import STR_MATCHES_REGEX


def test():
    assert STR_MATCHES_REGEX(re.compile("^abc")).matches("abc")
    assert STR_MATCHES_REGEX(re.compile("^abc$")).matches("abc")
    assert STR_MATCHES_REGEX(re.compile("abc$")).matches("abc")
    assert STR_MATCHES_REGEX(re.compile("^abc")).matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("abc")).matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("def")).matches("abcdef")
    assert STR_MATCHES_REGEX(re.compile("def$")).matches("abcdef")
    assert not STR_MATCHES_REGEX(re.compile("^def")).matches("abcdef")
