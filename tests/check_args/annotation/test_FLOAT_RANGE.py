import pytest

from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.FLOAT_RANGE import FLOAT_RANGE


def test_one_bound():
    assert not FLOAT_RANGE('>', 5.0).matches("abc")
    assert not FLOAT_RANGE('>', 5.0).matches(5)

    assert not FLOAT_RANGE('>', 5.0).matches(5.0)
    assert FLOAT_RANGE('>', 5.0).matches(6.0)

    assert not FLOAT_RANGE('>=', 5.0).matches(4.0)
    assert FLOAT_RANGE('>=', 5.0).matches(5.0)
    assert FLOAT_RANGE('>=', 5.0).matches(6.0)

    assert not FLOAT_RANGE('<', 5.0).matches(5.0)
    assert FLOAT_RANGE('<', 5.0).matches(4.0)

    assert not FLOAT_RANGE('<=', 5.0).matches(6.0)
    assert FLOAT_RANGE('<=', 5.0).matches(5.0)
    assert FLOAT_RANGE('<=', 5.0).matches(4.0)

    with pytest.raises(RCheckArgsError):
        FLOAT_RANGE('abc', 5.0, '>', 7.0)


def test_two_bounds():
    assert not FLOAT_RANGE('>', 5.0, '<', 7.0).matches("abc")
    assert FLOAT_RANGE('>', 5.0, '<', 7.0).matches(5.4321)

    assert not FLOAT_RANGE('>', 5.0, '<', 7.0).matches(5.0)
    assert FLOAT_RANGE('>', 5.0, '<', 7.0).matches(6.0)
    assert not FLOAT_RANGE('>', 5.0, '<', 7.0).matches(7.0)

    assert not FLOAT_RANGE('>=', 5.0, '<', 7.0).matches(4.0)
    assert FLOAT_RANGE('>=', 5.0, '<', 7.0).matches(5.0)
    assert FLOAT_RANGE('>=', 5.0, '<', 7.0).matches(6.0)
    assert not FLOAT_RANGE('>=', 5.0, '<', 7.0).matches(7.0)

    with pytest.raises(RCheckArgsError):
        FLOAT_RANGE('>=', 5.0, '>', 7.0)
