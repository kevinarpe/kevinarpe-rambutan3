from rambutan3.type.matcher.annotation.INSTANCE_OF import INSTANCE_OF


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


def test():
    assert not INSTANCE_OF(_Superclass).matches(_Superclass)
    assert INSTANCE_OF(_Superclass).matches(_Superclass())
    assert not INSTANCE_OF(_Superclass).matches("abc")
    assert not INSTANCE_OF(_Superclass).matches(_Subclass)
    assert INSTANCE_OF(_Superclass).matches(_Subclass())
    assert not INSTANCE_OF(_Superclass).matches(123)
    assert not INSTANCE_OF(_Subclass).matches(_Subclass)
    assert INSTANCE_OF(_Subclass).matches(_Subclass())
    assert not INSTANCE_OF(_Subclass).matches(_Superclass)
    assert not INSTANCE_OF(_Subclass).matches(_Superclass())
