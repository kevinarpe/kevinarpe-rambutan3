from rambutan3.check_args.annotation.BYTEARRAY import BYTEARRAY


def test():
    assert not BYTEARRAY.matches(b'abc')
    assert not BYTEARRAY.matches(bytes())
    assert BYTEARRAY.matches(bytearray())
    assert not BYTEARRAY.matches(memoryview(b''))
    assert not BYTEARRAY.matches('abc')
    assert not BYTEARRAY.matches(123)
