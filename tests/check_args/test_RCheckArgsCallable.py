import pytest
from rambutan3.check_args.RCheckArgs import check_args, _RCheckArgsCallable
from rambutan3.check_args.annotation.CLS import CLS
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError


@staticmethod
def blah():
    pass

class X:

    @check_args
    def dummy(self: SELF()):
        pass

    @check_args
    def dummy2(self: SELF(), z: SELF()):
        pass

    @check_args
    def dummy3(self: CLS()):
        pass

    @check_args
    @classmethod
    def dummy4(cls: CLS(), z: INT):
        pass

    @check_args
    @staticmethod
    def dummy5(z: INT):
        pass

    @staticmethod
    def dummy6(z):
        pass

    def dummy7(self, x):
        pass

    def dummy8(self: (123, 456)):
        pass

    @check_args
    def dummy9(self: SELF(), a: INT, *args: STR, **kwargs: FLOAT):
        pass

    @check_args
    def dummy10(self: SELF(), a: INT, b: INT, *, c: INT):
        pass

    def dummy11(self: SELF(), a: INT="abc"):
        pass

    @check_args
    def dummy12(self: SELF(), a: INT=123):
        pass

    @check_args
    @property
    def int_value(self: SELF()) -> INT:
        return 123

    @check_args
    @int_value.setter
    def int_value(self: SELF(), value: INT):
        pass

    @check_args
    @property
    def not_int_value(self: SELF()) -> INT:
        return "abc"

    @check_args
    def dummy14(self: SELF()):
        pass

    @check_args
    def dummy_prop(self: SELF()):
        pass

    def bad_return_type_matcher(self: SELF()) -> "abc":
        pass


def test():
    X().dummy()
    with pytest.raises(RCheckArgsError):
        X().dummy2(X())
    with pytest.raises(RCheckArgsError):
        X().dummy3()
    X.dummy4(123)
    X().dummy4(123)
    X.dummy6(123)
    X().dummy6(123)
    X.dummy5(123)
    X().dummy5(123)
    with pytest.raises(RCheckArgsError):
        X().dummy5(123, 456)
    with pytest.raises(RCheckArgsError):
        _RCheckArgsCallable(X.dummy7)
    with pytest.raises(RCheckArgsError):
        _RCheckArgsCallable(X.dummy8)
    X().dummy9(123, "def", "abc", "xyz", c=123.456)
    X().dummy10(123, 456, c=789)
    X().dummy10(a=123, b=456, c=789)
    X().dummy10(b=123, a=456, c=789)
    X().dummy10(c=123, a=456, b=789)
    with pytest.raises(RCheckArgsError):
        _RCheckArgsCallable(X.dummy11)
    X().dummy12()
    X().dummy12(123)
    X().dummy12(456)

    iv = X().int_value
    X().int_value = 123
    with pytest.raises(RCheckArgsError):
        X().int_value = "abc"
    with pytest.raises(RCheckArgsError):
        niv = X().not_int_value

    with pytest.raises(RCheckArgsError):
        # Cannot wrap twice
        check_args(X.dummy14)

    with pytest.raises(RCheckArgsError):
        p = property(X.dummy_prop)
        x = check_args(p)
        check_args(x)
        # Cannot wrap twice
        # check_args(X.dummy_prop)

    with pytest.raises(RCheckArgsError):
        check_args(X.bad_return_type_matcher)
