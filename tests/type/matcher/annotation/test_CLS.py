import pytest
from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.CLS import CLS
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.SELF import SELF
from rambutan3.type.matcher.error.RCheckArgsError import RCheckArgsError


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
    def method3(cls):
        pass

def test_method():
    # TODO: LAST: Weird behavior when passing cls or self to classmethod.
    # Need to add special handling.
    X.method3()
    X().method3()
    X.method()
    X().method()
    with pytest.raises(RCheckArgsError):
        X.method()
    with pytest.raises(RCheckArgsError):
        X.method(123)
    X.method(X())


def test_method2():
    X().method2(123)
    with pytest.raises(RCheckArgsError):
        X().method2("abc")
    with pytest.raises(RCheckArgsError):
        X.method2()
    with pytest.raises(RCheckArgsError):
        X.method2(123)
    with pytest.raises(RCheckArgsError):
        X.method2(123, "abc")
    X.method2(X(), 123)
