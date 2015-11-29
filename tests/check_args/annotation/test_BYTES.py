from rambutan3.check_args.annotation.BYTES import BYTES


def test():
    assert BYTES.matches(b'abc')
    assert BYTES.matches(bytes())
    assert not BYTES.matches(bytearray())
    assert not BYTES.matches(memoryview(b''))
    assert not BYTES.matches('abc')
    assert not BYTES.matches(123)
