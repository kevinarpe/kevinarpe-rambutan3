import re

import pytest

from rambutan3.type.string.RPatternText import RPatternText


__TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")


def test_ctor():
    with pytest.raises(TypeError):
        RPatternText(None, __TOKEN_PATTERN)
    with pytest.raises(TypeError):
        RPatternText(123, __TOKEN_PATTERN)
    with pytest.raises(ValueError):
        RPatternText("", __TOKEN_PATTERN)
    with pytest.raises(ValueError):
        RPatternText("   ", __TOKEN_PATTERN)
    assert "abc" == RPatternText("abc", __TOKEN_PATTERN).str
    assert "abc_def" == RPatternText("abc_def", __TOKEN_PATTERN).str
