import pytest

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError


class X:

    @check_args
    def method(self: SELF()):
        pass

    @check_args
    def method2(self: SELF(), data: INT):
        pass


def test_method():
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
