from rambutan3.check_args.annotation.BINARY_SEQUENCE import BINARY_SEQUENCE


def test():
    assert BINARY_SEQUENCE.matches(b'abc')
    assert BINARY_SEQUENCE.matches(bytes())
    assert BINARY_SEQUENCE.matches(bytearray())
    assert BINARY_SEQUENCE.matches(memoryview(b''))
    assert not BINARY_SEQUENCE.matches('abc')
    assert not BINARY_SEQUENCE.matches(123)
