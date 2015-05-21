from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher


def test_eq():
    assert RIterableOfMatcher(STR) == RIterableOfMatcher(STR)
    assert not(RIterableOfMatcher(STR) != RIterableOfMatcher(STR))
    assert not(RIterableOfMatcher(STR) == RIterableOfMatcher(INT))


def test_hash():
    assert hash(RIterableOfMatcher(STR)) == hash(RIterableOfMatcher(STR))
    assert not(hash(RIterableOfMatcher(STR)) == hash(RIterableOfMatcher(INT)))


def test_str():
    assert bool(str(RIterableOfMatcher(STR)))
    assert str(RIterableOfMatcher(STR)) == str(RIterableOfMatcher(STR))
    assert str(RIterableOfMatcher(STR)) != str(RIterableOfMatcher(INT))
