import pytest
from rambutan3.check_args.annotation.ANY_VALUE_OF import ANY_VALUE_OF


def test():
    with pytest.raises(ValueError):
        ANY_VALUE_OF()
    assert ANY_VALUE_OF(123).matches(123)
    assert ANY_VALUE_OF(123, "abc").matches(123)
    assert ANY_VALUE_OF(123, "abc").matches("abc")
    assert ANY_VALUE_OF(123, 456, 789).matches(123)
    assert not ANY_VALUE_OF(123, 456, 789).matches("abc")
    assert ANY_VALUE_OF(123, 456, "abc", 789).matches("abc")
    assert not ANY_VALUE_OF(123, "ABC").matches("abc")
