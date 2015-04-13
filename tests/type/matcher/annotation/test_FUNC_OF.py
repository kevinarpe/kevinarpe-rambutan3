import pytest
from rambutan3.type.matcher.annotation.BOOL import BOOL
from rambutan3.type.matcher.annotation.FUNC_OF import FUNC_OF
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.STR import STR


def dummy():
    pass


def dummy2(count: INT):
    pass


def dummy3(count: INT, name: STR) -> BOOL:
    pass


def test():
    assert FUNC_OF().returnsNothing().matches(dummy)
    assert not FUNC_OF().returnsNothing().matches(dummy2)
    assert not FUNC_OF().returnsNothing().matches(dummy3)
    assert FUNC_OF(INT).returnsNothing().matches(dummy2)
    assert not FUNC_OF(INT).returnsNothing().matches(dummy)
    assert not FUNC_OF(INT).returnsNothing().matches(dummy3)
    assert FUNC_OF(INT, STR).returns(BOOL).matches(dummy3)
    assert not FUNC_OF(INT, STR).returns(BOOL).matches(dummy)
    assert not FUNC_OF(INT, STR).returns(BOOL).matches(dummy2)
    assert not FUNC_OF().returnsNothing().matches(None)
    assert not FUNC_OF(INT).returnsNothing().matches(None)
    assert not FUNC_OF(INT).returns(BOOL).matches(None)
    assert not FUNC_OF().returnsNothing().matches(123)
    assert not FUNC_OF(INT).returnsNothing().matches(123)
    assert not FUNC_OF(INT).returns(BOOL).matches(123)
    assert not FUNC_OF().returnsNothing().matches([])
    assert not FUNC_OF(INT).returnsNothing().matches([])
    assert not FUNC_OF(INT).returns(BOOL).matches([])
    with pytest.raises(TypeError):
        FUNC_OF().matches(dummy)
