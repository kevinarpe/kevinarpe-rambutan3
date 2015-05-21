import pytest

from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.POSITIVE_INT import POSITIVE_INT
from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError
from rambutan3.container.RFullTypedEnumDict import RFullTypedEnumDict
from rambutan3.enumeration.RTypedEnum import RTypedEnum
from rambutan3.string.RMessageText import RMessageText


class _AttrEnum(RTypedEnum):

    A = POSITIVE_INT
    B = INSTANCE_OF(RMessageText)


def test():
    with pytest.raises(RCheckArgsError):
        RFullTypedEnumDict()

    with pytest.raises(RCheckArgsError):
        RFullTypedEnumDict("abc")

    with pytest.raises(ValueError):
        RFullTypedEnumDict(key_type=_AttrEnum, dictionary={})

    with pytest.raises(ValueError):
        RFullTypedEnumDict(key_type=_AttrEnum, dictionary={_AttrEnum.A: "abc"})

    with pytest.raises(RCheckArgsError):
        RFullTypedEnumDict(key_type=_AttrEnum, dictionary={_AttrEnum.A: "abc", _AttrEnum.B: "def"})

    d = RFullTypedEnumDict(key_type=_AttrEnum, dictionary={_AttrEnum.A: 123, _AttrEnum.B: RMessageText("def")})

    with pytest.raises(RCheckArgsError):
        d[_AttrEnum.A] = "abc"

    d[_AttrEnum.A] = 456
    assert d[_AttrEnum.A] is 456

    with pytest.raises(AttributeError):
        del d[_AttrEnum.B]

    with pytest.raises(AttributeError):
        d.clear()
