import pytest

from rambutan3.type.string.RNonEmptyStr import RNonEmptyStr


def test_ctor():
    with pytest.raises(TypeError):
        RNonEmptyStr(None)
    with pytest.raises(TypeError):
        RNonEmptyStr(123)
    with pytest.raises(ValueError):
        RNonEmptyStr("")
    assert "abc" == RNonEmptyStr("abc").str
    assert "abc  " == RNonEmptyStr("abc  ").str
    assert "  abc  " == RNonEmptyStr("  abc  ").str
    assert "  " == RNonEmptyStr("  ").str
