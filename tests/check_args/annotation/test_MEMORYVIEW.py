from rambutan3.check_args.annotation.MEMORYVIEW import MEMORYVIEW


def test():
    assert not MEMORYVIEW.matches(b'abc')
    assert not MEMORYVIEW.matches(bytes())
    assert not MEMORYVIEW.matches(bytearray())
    assert MEMORYVIEW.matches(memoryview(b''))
    assert not MEMORYVIEW.matches('abc')
    assert not MEMORYVIEW.matches(123)
