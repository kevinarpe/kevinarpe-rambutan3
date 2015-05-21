from rambutan3.check_args.iter.RIterableMatcher import RIterableMatcher


def test_eq():
    assert RIterableMatcher() == RIterableMatcher()
    assert not(RIterableMatcher() != RIterableMatcher())


def test_hash():
    assert hash(RIterableMatcher()) == hash(RIterableMatcher())


def test_str():
    assert bool(str(RIterableMatcher()))
    assert str(RIterableMatcher()) == str(RIterableMatcher())
