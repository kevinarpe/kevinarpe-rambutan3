import pytest
from rambutan3.string.RIdentifier import RIdentifier


def test_ctor():
    with pytest.raises(TypeError):
        RIdentifier(None)
    with pytest.raises(TypeError):
        RIdentifier(123)
    with pytest.raises(ValueError):
        RIdentifier("")
    with pytest.raises(ValueError):
        RIdentifier("   ")
    assert "abc" == RIdentifier("abc")
    assert "abc_def" == RIdentifier("abc_def")
