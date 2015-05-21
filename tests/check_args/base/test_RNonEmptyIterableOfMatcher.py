from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.iter.RNonEmptyIterableOfMatcher import RNonEmptyIterableOfMatcher


def test_eq():
    assert RNonEmptyIterableOfMatcher(STR) == RNonEmptyIterableOfMatcher(STR)
    assert not(RNonEmptyIterableOfMatcher(STR) != RNonEmptyIterableOfMatcher(STR))
    assert not(RNonEmptyIterableOfMatcher(STR) == RNonEmptyIterableOfMatcher(INT))


def test_hash():
    assert hash(RNonEmptyIterableOfMatcher(STR)) == hash(RNonEmptyIterableOfMatcher(STR))
    assert not(hash(RNonEmptyIterableOfMatcher(STR)) == hash(RNonEmptyIterableOfMatcher(INT)))


def test_str():
    assert bool(str(RNonEmptyIterableOfMatcher(STR)))
    assert str(RNonEmptyIterableOfMatcher(STR)) == str(RNonEmptyIterableOfMatcher(STR))
    assert str(RNonEmptyIterableOfMatcher(STR)) != str(RNonEmptyIterableOfMatcher(INT))
