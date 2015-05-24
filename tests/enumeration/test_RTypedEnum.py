import pytest

from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.enumeration.RTypedEnum import RTypedEnum


def test():
    class _GoodRTypedEnum(RTypedEnum):
        a = INT
        b = STR
        c = BOOL

    with pytest.raises(RCheckArgsError):
        class _BadRTypedEnum(RTypedEnum):
            a = INT
            b = "xyz"
            c = BOOL

    with pytest.raises(RCheckArgsError):
        class _BadRTypedEnum2(RTypedEnum):
            a = INT
            b = None
            c = BOOL
