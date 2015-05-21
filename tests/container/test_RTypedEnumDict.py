import pytest

from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.POSITIVE_INT import POSITIVE_INT
from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError
from rambutan3.container.RTypedEnumDict import RTypedEnumDict
from rambutan3.enumeration.RTypedEnum import RTypedEnum
from rambutan3.string.RMessageText import RMessageText


class _AttrEnum(RTypedEnum):

    A = POSITIVE_INT
    B = INSTANCE_OF(RMessageText)


def test():
    with pytest.raises(RCheckArgsError):
        RTypedEnumDict()

    with pytest.raises(RCheckArgsError):
        RTypedEnumDict("abc")

    d = RTypedEnumDict(_AttrEnum)

    with pytest.raises(RCheckArgsError):
        d[_AttrEnum.A] = "abc"

    d[_AttrEnum.A] = 3

    with pytest.raises(RCheckArgsError):
        d[_AttrEnum.B] = 123

    d[_AttrEnum.B] = RMessageText("abc")

    with pytest.raises(RCheckArgsError):
        d["abc"] = "xyz"

    with pytest.raises(RCheckArgsError):
        RTypedEnumDict(_AttrEnum, {_AttrEnum.A: "abc"})

    RTypedEnumDict(_AttrEnum, {_AttrEnum.A: 123})

    RTypedEnumDict(_AttrEnum, {_AttrEnum.B: RMessageText("abc"), _AttrEnum.A: 123})
