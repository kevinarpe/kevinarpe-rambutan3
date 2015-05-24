from rambutan3.check_args.annotation.INSTANCE_BY_TYPE_NAME import INSTANCE_BY_TYPE_NAME


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


def test():
    assert not INSTANCE_BY_TYPE_NAME('_Superclass').matches(_Superclass)
    assert INSTANCE_BY_TYPE_NAME('_Superclass').matches(_Superclass())
    assert not INSTANCE_BY_TYPE_NAME('_Superclass').matches("abc")
    assert not INSTANCE_BY_TYPE_NAME('_Superclass').matches(_Subclass)
    assert not INSTANCE_BY_TYPE_NAME('_Superclass').matches(_Subclass())
    assert not INSTANCE_BY_TYPE_NAME('_Superclass').matches(123)
    assert not INSTANCE_BY_TYPE_NAME('_Subclass').matches(_Subclass)
    assert INSTANCE_BY_TYPE_NAME('_Subclass').matches(_Subclass())
    assert not INSTANCE_BY_TYPE_NAME('_Subclass').matches(_Superclass)
    assert not INSTANCE_BY_TYPE_NAME('_Subclass').matches(_Superclass())
