import pytest

from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.NUMBER_RANGE import NUMBER_RANGE


def test_one_bound():
    assert not NUMBER_RANGE('>', 5).matches("abc")
    assert not NUMBER_RANGE('>', 5.0).matches("abc")
    assert NUMBER_RANGE('>', 5).matches(5.4321)
    assert NUMBER_RANGE('>', 5.0).matches(5.4321)

    assert not NUMBER_RANGE('>', 5).matches(5)
    assert not NUMBER_RANGE('>', 5.0).matches(5)
    assert not NUMBER_RANGE('>', 5).matches(5.0)
    assert not NUMBER_RANGE('>', 5.0).matches(5.0)
    assert NUMBER_RANGE('>', 5).matches(6)
    assert NUMBER_RANGE('>', 5.0).matches(6)
    assert NUMBER_RANGE('>', 5).matches(6.0)
    assert NUMBER_RANGE('>', 5.0).matches(6.0)

    assert not NUMBER_RANGE('>=', 5).matches(4)
    assert not NUMBER_RANGE('>=', 5.0).matches(4)
    assert not NUMBER_RANGE('>=', 5).matches(4.0)
    assert not NUMBER_RANGE('>=', 5.0).matches(4.0)
    assert NUMBER_RANGE('>=', 5).matches(5)
    assert NUMBER_RANGE('>=', 5.0).matches(5)
    assert NUMBER_RANGE('>=', 5).matches(5.0)
    assert NUMBER_RANGE('>=', 5.0).matches(5.0)
    assert NUMBER_RANGE('>=', 5).matches(6)
    assert NUMBER_RANGE('>=', 5.0).matches(6)
    assert NUMBER_RANGE('>=', 5).matches(6.0)
    assert NUMBER_RANGE('>=', 5.0).matches(6.0)

    assert not NUMBER_RANGE('<', 5).matches(5)
    assert not NUMBER_RANGE('<', 5.0).matches(5)
    assert not NUMBER_RANGE('<', 5).matches(5.0)
    assert not NUMBER_RANGE('<', 5.0).matches(5.0)
    assert NUMBER_RANGE('<', 5).matches(4)
    assert NUMBER_RANGE('<', 5.0).matches(4)
    assert NUMBER_RANGE('<', 5).matches(4.0)
    assert NUMBER_RANGE('<', 5.0).matches(4.0)

    assert not NUMBER_RANGE('<=', 5).matches(6)
    assert not NUMBER_RANGE('<=', 5).matches(6)
    assert not NUMBER_RANGE('<=', 5).matches(6.0)
    assert not NUMBER_RANGE('<=', 5).matches(6.0)
    assert NUMBER_RANGE('<=', 5).matches(5)
    assert NUMBER_RANGE('<=', 5.0).matches(5)
    assert NUMBER_RANGE('<=', 5).matches(5.0)
    assert NUMBER_RANGE('<=', 5.0).matches(5.0)
    assert NUMBER_RANGE('<=', 5).matches(4)
    assert NUMBER_RANGE('<=', 5.0).matches(4)
    assert NUMBER_RANGE('<=', 5).matches(4.0)
    assert NUMBER_RANGE('<=', 5.0).matches(4.0)

    with pytest.raises(RCheckArgsError):
        NUMBER_RANGE('abc', 5, '>', 7)


def test_two_bounds():
    assert not NUMBER_RANGE('>', 5, '<', 7).matches("abc")
    assert not NUMBER_RANGE('>', 5.0, '<', 7).matches("abc")
    assert not NUMBER_RANGE('>', 5, '<', 7.0).matches("abc")
    assert not NUMBER_RANGE('>', 5.0, '<', 7.0).matches("abc")
    assert NUMBER_RANGE('>', 5, '<', 7).matches(5.4321)
    assert NUMBER_RANGE('>', 5.0, '<', 7).matches(5.4321)
    assert NUMBER_RANGE('>', 5, '<', 7.0).matches(5.4321)
    assert NUMBER_RANGE('>', 5.0, '<', 7.0).matches(5.4321)

    assert not NUMBER_RANGE('>', 5, '<', 7).matches(5)
    assert not NUMBER_RANGE('>', 5.0, '<', 7).matches(5)
    assert not NUMBER_RANGE('>', 5, '<', 7.0).matches(5)
    assert not NUMBER_RANGE('>', 5.0, '<', 7.0).matches(5)
    assert NUMBER_RANGE('>', 5, '<', 7).matches(6)
    assert NUMBER_RANGE('>', 5.0, '<', 7).matches(6)
    assert NUMBER_RANGE('>', 5, '<', 7.0).matches(6)
    assert NUMBER_RANGE('>', 5.0, '<', 7.0).matches(6)
    assert not NUMBER_RANGE('>', 5, '<', 7).matches(7)
    assert not NUMBER_RANGE('>', 5.0, '<', 7).matches(7)
    assert not NUMBER_RANGE('>', 5, '<', 7.0).matches(7)
    assert not NUMBER_RANGE('>', 5.0, '<', 7.0).matches(7)

    assert not NUMBER_RANGE('>=', 5, '<', 7).matches(4)
    assert not NUMBER_RANGE('>=', 5.0, '<', 7).matches(4)
    assert not NUMBER_RANGE('>=', 5, '<', 7.0).matches(4)
    assert not NUMBER_RANGE('>=', 5.0, '<', 7.0).matches(4)
    assert NUMBER_RANGE('>=', 5, '<', 7).matches(5)
    assert NUMBER_RANGE('>=', 5.0, '<', 7).matches(5)
    assert NUMBER_RANGE('>=', 5, '<', 7.0).matches(5)
    assert NUMBER_RANGE('>=', 5.0, '<', 7.0).matches(5)
    assert NUMBER_RANGE('>=', 5, '<', 7).matches(6)
    assert NUMBER_RANGE('>=', 5.0, '<', 7).matches(6)
    assert NUMBER_RANGE('>=', 5, '<', 7.0).matches(6)
    assert NUMBER_RANGE('>=', 5.0, '<', 7.0).matches(6)
    assert not NUMBER_RANGE('>=', 5, '<', 7).matches(7)
    assert not NUMBER_RANGE('>=', 5.0, '<', 7).matches(7)
    assert not NUMBER_RANGE('>=', 5, '<', 7.0).matches(7)
    assert not NUMBER_RANGE('>=', 5.0, '<', 7.0).matches(7)

    with pytest.raises(RCheckArgsError):
        NUMBER_RANGE('>=', 5, '>', 7)
