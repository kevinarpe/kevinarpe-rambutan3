import pytest
from rambutan3.string.RVariableName import RVariableName


def test_ctor():
    with pytest.raises(TypeError):
        RVariableName(None)
    with pytest.raises(TypeError):
        RVariableName(123)
    with pytest.raises(ValueError):
        RVariableName("")
    with pytest.raises(ValueError):
        RVariableName("   ")
    assert "abc" == RVariableName("abc")
    assert "abc_def" == RVariableName("abc_def")
