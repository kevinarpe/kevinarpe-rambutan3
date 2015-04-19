import pytest

from rambutan3.check_args.annotation.RANGE_SIZE_LIST import RANGE_SIZE_LIST


def test():
    assert RANGE_SIZE_LIST(min_size=0).matches([])
    assert RANGE_SIZE_LIST(min_size=0, max_size=3).matches([])
    assert RANGE_SIZE_LIST(max_size=3, min_size=0).matches([])
    assert not RANGE_SIZE_LIST(min_size=3).matches([])
    assert RANGE_SIZE_LIST(min_size=3).matches([123, "abc", True])
    assert RANGE_SIZE_LIST(max_size=0).matches([])
    assert not RANGE_SIZE_LIST(max_size=1).matches([123, "abc", True])
    assert not RANGE_SIZE_LIST(max_size=1).matches([123, "abc"])
    assert RANGE_SIZE_LIST(max_size=1).matches([123])
    assert not RANGE_SIZE_LIST(min_size=2, max_size=7).matches("abc")
    assert not RANGE_SIZE_LIST(min_size=2, max_size=7).matches(None)
    assert not RANGE_SIZE_LIST(min_size=2, max_size=7).matches(tuple())
    assert not RANGE_SIZE_LIST(min_size=2, max_size=7).matches((1, 2, 3))
    with pytest.raises(ValueError):
        RANGE_SIZE_LIST()
    with pytest.raises(ValueError):
        RANGE_SIZE_LIST(min_size=-1, max_size=-1)
    with pytest.raises(ValueError):
        RANGE_SIZE_LIST(min_size=3, max_size=2)
    with pytest.raises(ValueError):
        RANGE_SIZE_LIST(min_size=-3, max_size=2)
    with pytest.raises(ValueError):
        RANGE_SIZE_LIST(min_size=3, max_size=-2)
