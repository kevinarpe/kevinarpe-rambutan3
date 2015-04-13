import pytest
from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.CLS import CLS
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.SELF import SELF
from rambutan3.type.matcher.error.RCheckArgsError import RCheckArgsError


# def test_blah():
#     e = None
#     try:
#         raise ValueError("yat")
#     except Exception as e:
#         pass
#     if e:
#         print("yi")


class X:

    @check_args
    @classmethod
    def method(cls: CLS()):
        pass

    @check_args
    @classmethod
    def method2(cls: CLS(), data: INT):
        pass

    @classmethod
    def naked_method(cls):
        pass

    @classmethod
    def naked_method2(cls, data: int):
        pass


def test_naked_method():
    X.naked_method()
    X().naked_method()
    with pytest.raises(TypeError):
        X.naked_method(123)
    with pytest.raises(TypeError):
        X.naked_method(X())
    with pytest.raises(TypeError):
        X().naked_method(X())


def test_method():
    X.method()
    X().method()
    with pytest.raises(RCheckArgsError):
        X.method(123)
    with pytest.raises(RCheckArgsError):
        X.method(X())
    with pytest.raises(RCheckArgsError):
        X().method(X())


def test_naked_method2():
    X.naked_method2(123)
    X().naked_method2(123)
    X.naked_method2("abc")
    X().naked_method2("abc")
    with pytest.raises(TypeError):
        X.naked_method2()
    with pytest.raises(TypeError):
        X().naked_method2()
    with pytest.raises(TypeError):
        X.naked_method2(123, "abc")
    with pytest.raises(TypeError):
        X().naked_method2(123, "abc")
    with pytest.raises(TypeError):
        X.naked_method2(X(), 123)
    with pytest.raises(TypeError):
        X().naked_method2(X(), 123)


def test_method2():
    X.method2(123)
    X().method2(123)
    with pytest.raises(RCheckArgsError):
        X.method2("abc")
    with pytest.raises(RCheckArgsError):
        X().method2("abc")
    with pytest.raises(RCheckArgsError):
        X.method2()
    with pytest.raises(RCheckArgsError):
        X().method2()
    with pytest.raises(RCheckArgsError):
        X.method2(123, "abc")
    with pytest.raises(RCheckArgsError):
        X().method2(123, "abc")
    with pytest.raises(RCheckArgsError):
        X.method2(X(), 123)
    with pytest.raises(RCheckArgsError):
        X().method2(X(), 123)
