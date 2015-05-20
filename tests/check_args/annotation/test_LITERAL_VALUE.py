import pytest
from rambutan3.check_args.annotation.LITERAL_VALUE import LITERAL_VALUE


def test():
    with pytest.raises(TypeError):
        LITERAL_VALUE()

    assert LITERAL_VALUE(123).matches(123)

    with pytest.raises(TypeError):
        assert LITERAL_VALUE(123, "abc").matches(123)

    assert LITERAL_VALUE("abc").matches("abc")
    assert not LITERAL_VALUE("ABC").matches("abc")
    assert LITERAL_VALUE(("abc", 123)).matches(("abc", 123))
