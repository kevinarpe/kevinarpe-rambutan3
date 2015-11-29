import pytest

from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.base.RNotNoneTypeMatcher import RNotNoneTypeMatcher


def test_ctor():
    RNotNoneTypeMatcher()

    with pytest.raises(TypeError):
        RNotNoneTypeMatcher(123)


def test_check_arg():
    __check_arg('abc', is_ok=True)
    __check_arg(123, is_ok=True)
    __check_arg(True, is_ok=True)
    __check_arg(123.456, is_ok=True)
    __check_arg([123], is_ok=True)
    __check_arg(None, is_ok=False)
    __check_arg([None], is_ok=True)


def __check_arg(value, *, is_ok: bool):
    m = RNotNoneTypeMatcher()
    if is_ok:
        assert m.check_arg(value, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(value, 'dummy_arg_name')


def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(RNotNoneTypeMatcher(), RNotNoneTypeMatcher(), is_equal=True)
    RTestUtil.test_eq_ne_hash(RNotNoneTypeMatcher(), INT | RNotNoneTypeMatcher(), is_equal=False)


def test__str__():
    assert str(RNotNoneTypeMatcher()) == 'not None'
