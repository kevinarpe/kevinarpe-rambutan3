import re

import pytest
from rambutan3.string.RPatternText import RPatternText


__TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")


def test_ctor():
    with pytest.raises(NotImplementedError):
        RPatternText("abc")  # do not call ctor directly
    with pytest.raises(TypeError):
        RPatternText.new(None, __TOKEN_PATTERN)
    with pytest.raises(TypeError):
        RPatternText.new(123, __TOKEN_PATTERN)
    with pytest.raises(ValueError):
        RPatternText.new("", __TOKEN_PATTERN)
    with pytest.raises(ValueError):
        RPatternText.new("   ", __TOKEN_PATTERN)
    assert "abc" == RPatternText.new("abc", __TOKEN_PATTERN)
    assert "abc_def" == RPatternText.new("abc_def", __TOKEN_PATTERN)
