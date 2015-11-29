import re

import pytest
from rambutan3.string.RMessageText import RMessageText
from rambutan3.string.RPatternText import RPatternText


__TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")
__HUMAN_READABLE_HINT = RMessageText('strict identifier, e.g., ClassName or var_name3')

def test_ctor():
    with pytest.raises(NotImplementedError):
        RPatternText("abc")  # do not call ctor directly
    with pytest.raises(TypeError):
        RPatternText.new(None, __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
    with pytest.raises(TypeError):
        RPatternText.new(123, __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
    with pytest.raises(ValueError):
        RPatternText.new("", __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
    with pytest.raises(ValueError):
        RPatternText.new("   ", __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
    with pytest.raises(TypeError):
        RPatternText.new("abc", "not regex pattern type", __HUMAN_READABLE_HINT)
    with pytest.raises(TypeError):
        RPatternText.new("abc", __TOKEN_PATTERN, "not type RMessageText")

    assert "abc" == RPatternText.new("abc", __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
    assert "abc_def" == RPatternText.new("abc_def", __TOKEN_PATTERN, __HUMAN_READABLE_HINT)
