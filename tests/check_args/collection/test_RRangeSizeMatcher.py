import pytest

from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.collection.RRangeSizeMatcher import RRangeSizeMatcher


def test_ctor():
    core_test_ctor(RRangeSizeMatcher)


def core_test_ctor(ctor_func):
    with pytest.raises(ValueError):
        ctor_func()

    with pytest.raises(TypeError):
        ctor_func('abc')

    with pytest.raises(TypeError):
        ctor_func(123)

    with pytest.raises(TypeError):
        ctor_func(['abc'])

    ctor_func(min_size=0)
    ctor_func(min_size=-1, max_size=3)
    ctor_func(min_size=3, max_size=-1)

    with pytest.raises(ValueError):
        ctor_func(min_size=-2)

    with pytest.raises(ValueError):
        ctor_func(min_size=-2, max_size=3)

    with pytest.raises(ValueError):
        ctor_func(max_size=-2)

    with pytest.raises(ValueError):
        ctor_func(max_size=-2, min_size=3)

    ctor_func(min_size=8)

    ctor_func(min_size=8, max_size=15)

    ctor_func(min_size=8, max_size=8)

    with pytest.raises(ValueError):
        ctor_func(min_size=8, max_size=7)

    ctor_func(max_size=8)

    with pytest.raises(ValueError):
        ctor_func(min_size=-8)

    with pytest.raises(ValueError):
        ctor_func(max_size=-8)

    with pytest.raises(ValueError):
        ctor_func(min_size=8, max_size=-7)

    with pytest.raises(ValueError):
        ctor_func(min_size=-8, max_size=7)


def test_check_arg():
    __check_arg([123], min_size=1)
    __check_arg([123], max_size=1)
    __check_arg([123], min_size=1, max_size=2)

    with pytest.raises(RCheckArgsError):
        __check_arg(None, min_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg(123, min_size=1)

    __check_arg('abc', min_size=1)

    with pytest.raises(RCheckArgsError):
        __check_arg('abc', min_size=4)

    __check_arg('abc', max_size=3)

    with pytest.raises(RCheckArgsError):
        __check_arg('abc', max_size=2)

    with pytest.raises(RCheckArgsError):
        __check_arg('', min_size=1, max_size=3)

    __check_arg('a', min_size=1, max_size=3)
    __check_arg('ab', min_size=1, max_size=3)
    __check_arg('abc', min_size=1, max_size=3)

    with pytest.raises(RCheckArgsError):
        __check_arg('abcd', min_size=1, max_size=3)


def __check_arg(value, *, min_size: int=-1, max_size: int=-1):
    m = RRangeSizeMatcher(min_size=min_size, max_size=max_size)
    assert value is m.check_arg(value, 'dummy_arg_name')


def test__eq__and__ne__():
    core_test__eq__and__ne__(RRangeSizeMatcher)


def core_test__eq__and__ne__(ctor_func):
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1), 'abc', is_equal=False)
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1), ctor_func(min_size=1), is_equal=True)
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1, max_size=2),
                             ctor_func(min_size=1, max_size=7),
                             is_equal=False)
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1, max_size=7),
                             ctor_func(min_size=4, max_size=7),
                             is_equal=False)
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1, max_size=2),
                             ctor_func(min_size=4, max_size=7),
                             is_equal=False)
    RTestUtil.test_eq_ne_hash(ctor_func(min_size=1, max_size=2),
                             ctor_func(min_size=1, max_size=2),
                             is_equal=True)


def test__hash__():
    core_test__hash__(RRangeSizeMatcher)


def core_test__hash__(ctor_func):
    assert hash(ctor_func(min_size=1)) == hash(ctor_func(min_size=1))
    assert hash(ctor_func(min_size=1)) != hash(ctor_func(min_size=4))

    assert hash(ctor_func(min_size=1, max_size=2)) \
           == \
           hash(ctor_func(min_size=1, max_size=2))

    assert hash(ctor_func(min_size=1, max_size=3)) \
           != \
           hash(ctor_func(min_size=1, max_size=2))

    assert hash(ctor_func(min_size=1, max_size=3)) \
           != \
           hash(ctor_func(min_size=2, max_size=3))

    assert hash(ctor_func(min_size=1, max_size=2)) != hash(ctor_func(min_size=1))
    assert hash(ctor_func(min_size=1, max_size=2)) != hash(ctor_func(min_size=4))


def test__str__():
    assert str(RRangeSizeMatcher(min_size=1)) == ' where size >= 1'
    assert str(RRangeSizeMatcher(max_size=1)) == ' where size <= 1'
    assert str(RRangeSizeMatcher(min_size=1, max_size=2)) == ' where size >= 1 and size <= 2'
