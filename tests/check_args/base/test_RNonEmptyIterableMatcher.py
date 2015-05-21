from rambutan3.check_args.iter.RNonEmptyIterableMatcher import RNonEmptyIterableMatcher


def test_eq():
    assert RNonEmptyIterableMatcher() == RNonEmptyIterableMatcher()
    assert not(RNonEmptyIterableMatcher() != RNonEmptyIterableMatcher())


def test_hash():
    assert hash(RNonEmptyIterableMatcher()) == hash(RNonEmptyIterableMatcher())


def test_str():
    assert bool(str(RNonEmptyIterableMatcher()))
    assert str(RNonEmptyIterableMatcher()) == str(RNonEmptyIterableMatcher())
