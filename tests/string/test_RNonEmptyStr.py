import pytest
from rambutan3.string.RNonEmptyStr import RNonEmptyStr


def test_ctor():
    with pytest.raises(TypeError):
        RNonEmptyStr(None)
    with pytest.raises(TypeError):
        RNonEmptyStr(123)
    with pytest.raises(ValueError):
        RNonEmptyStr("")
    assert "abc" == RNonEmptyStr("abc")
    assert "abc  " == RNonEmptyStr("abc  ")
    assert "  abc  " == RNonEmptyStr("  abc  ")
    assert "  " == RNonEmptyStr("  ")
