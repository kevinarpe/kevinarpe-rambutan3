from rambutan3 import RArgs, RIterableUtil


def test_is_iterable():
    assert not RIterableUtil.is_iterable(None)
    assert not RIterableUtil.is_iterable('abc')
    assert not RIterableUtil.is_iterable(123)
    assert RIterableUtil.is_iterable([])
    assert RIterableUtil.is_iterable(dict())
    assert RIterableUtil.is_iterable(set())
    assert RIterableUtil.is_iterable([123])


def test_make_iterable():
    __test_make_iterable(None)
    __test_make_iterable('abc')
    __test_make_iterable(123)
    __test_make_iterable([])
    __test_make_iterable(dict())
    __test_make_iterable(set())
    __test_make_iterable([123])


def __test_make_iterable(value):
    RArgs.check_is_iterable(RIterableUtil.make_iterable(value), 'dummy_arg_name')
