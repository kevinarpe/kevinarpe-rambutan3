import pytest

from rambutan3.type.string.RMessageText import RMessageText


def test_ctor():
    with pytest.raises(TypeError):
        RMessageText(None)
    with pytest.raises(TypeError):
        RMessageText(123)
    with pytest.raises(ValueError):
        RMessageText("")
    with pytest.raises(ValueError):
        RMessageText("   ")
    assert "abc" == RMessageText("abc").str
    assert "abc  " == RMessageText("abc  ").str
    assert "  abc  " == RMessageText("  abc  ").str
