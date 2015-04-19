from rambutan3.check_args.annotation.SUBCLASS_OF import SUBCLASS_OF


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


def test():
    assert SUBCLASS_OF(_Superclass).matches(_Superclass)
    assert not SUBCLASS_OF(_Superclass).matches(_Superclass())
    assert not SUBCLASS_OF(_Superclass).matches("abc")
    assert SUBCLASS_OF(_Superclass).matches(_Subclass)
    assert not SUBCLASS_OF(_Superclass).matches(_Subclass())
    assert not SUBCLASS_OF(_Superclass).matches(123)
    assert SUBCLASS_OF(_Subclass).matches(_Subclass)
    assert not SUBCLASS_OF(_Subclass).matches(_Superclass)
