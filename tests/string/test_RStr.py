import pytest
from rambutan3.string.RStr import RStr


def test_ctor():
    str(None) == RStr(None)
    str(123) == RStr(123)
    str("abc") == RStr("abc")
    str("") == RStr("")


def test_iter():
    with pytest.raises(TypeError):
        iter(RStr("abc"))
    x = RStr("abc").iter()