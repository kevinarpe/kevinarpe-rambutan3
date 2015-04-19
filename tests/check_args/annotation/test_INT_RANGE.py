import pytest

from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.INT_RANGE import INT_RANGE


def test_one_bound():
    assert not INT_RANGE('>', 5).matches("abc")
    assert not INT_RANGE('>', 5).matches(5.4321)

    assert not INT_RANGE('>', 5).matches(5)
    assert INT_RANGE('>', 5).matches(6)

    assert not INT_RANGE('>=', 5).matches(4)
    assert INT_RANGE('>=', 5).matches(5)
    assert INT_RANGE('>=', 5).matches(6)

    assert not INT_RANGE('<', 5).matches(5)
    assert INT_RANGE('<', 5).matches(4)

    assert not INT_RANGE('<=', 5).matches(6)
    assert INT_RANGE('<=', 5).matches(5)
    assert INT_RANGE('<=', 5).matches(4)

    with pytest.raises(RCheckArgsError):
        INT_RANGE('abc', 5, '>', 7)

    # bool is a subclass of int, but do not match!
    assert not INT_RANGE('>=', 0).matches(True)


def test_two_bounds():
    assert not INT_RANGE('>', 5, '<', 7).matches("abc")
    assert not INT_RANGE('>', 5, '<', 7).matches(5.4321)

    assert not INT_RANGE('>', 5, '<', 7).matches(5)
    assert INT_RANGE('>', 5, '<', 7).matches(6)
    assert not INT_RANGE('>', 5, '<', 7).matches(7)

    assert not INT_RANGE('>=', 5, '<', 7).matches(4)
    assert INT_RANGE('>=', 5, '<', 7).matches(5)
    assert INT_RANGE('>=', 5, '<', 7).matches(6)
    assert not INT_RANGE('>=', 5, '<', 7).matches(7)

    with pytest.raises(RCheckArgsError):
        INT_RANGE('>=', 5, '>', 7)

    # bool is a subclass of int, but do not match!
    assert not INT_RANGE('>=', 0, '<=', 1).matches(True)
