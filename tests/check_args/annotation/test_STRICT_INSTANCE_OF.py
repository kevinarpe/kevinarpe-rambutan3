from rambutan3.check_args.annotation.STRICT_INSTANCE_OF import STRICT_INSTANCE_OF


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


def test():
    assert not STRICT_INSTANCE_OF(_Superclass).matches(_Superclass)
    assert STRICT_INSTANCE_OF(_Superclass).matches(_Superclass())
    assert not STRICT_INSTANCE_OF(_Superclass).matches("abc")
    assert not STRICT_INSTANCE_OF(_Superclass).matches(_Subclass)
    assert not STRICT_INSTANCE_OF(_Superclass).matches(_Subclass())
    assert not STRICT_INSTANCE_OF(_Superclass).matches(123)
    assert not STRICT_INSTANCE_OF(_Subclass).matches(_Subclass)
    assert STRICT_INSTANCE_OF(_Subclass).matches(_Subclass())
    assert not STRICT_INSTANCE_OF(_Subclass).matches(_Superclass)
    assert not STRICT_INSTANCE_OF(_Subclass).matches(_Superclass())
