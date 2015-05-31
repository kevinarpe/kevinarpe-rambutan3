import pytest
from rambutan3.string.RStrictIdentifier import RStrictIdentifier


def test_ctor():
    with pytest.raises(TypeError):
        RStrictIdentifier(None)
    with pytest.raises(TypeError):
        RStrictIdentifier(123)
    with pytest.raises(ValueError):
        RStrictIdentifier("")
    with pytest.raises(ValueError):
        RStrictIdentifier("   ")
    assert "abc" == RStrictIdentifier("abc")
    assert "abc_def" == RStrictIdentifier("abc_def")
