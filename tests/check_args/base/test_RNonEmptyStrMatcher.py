from rambutan3.check_args.base.RNonEmptyStrMatcher import RNonEmptyStrMatcher


def test_eq():
    assert RNonEmptyStrMatcher() == RNonEmptyStrMatcher()
    assert not(RNonEmptyStrMatcher() != RNonEmptyStrMatcher())


def test_hash():
    assert hash(RNonEmptyStrMatcher()) == hash(RNonEmptyStrMatcher())


def test_str():
    assert bool(str(RNonEmptyStrMatcher()))
    assert str(RNonEmptyStrMatcher()) == str(RNonEmptyStrMatcher())
