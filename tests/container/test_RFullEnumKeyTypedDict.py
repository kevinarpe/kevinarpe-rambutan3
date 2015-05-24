import pytest

from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.container.RFullEnumKeyTypedDict import RFullEnumKeyTypedDict
from rambutan3.enumeration.REnum import REnum


class _AttrEnum(REnum):

    A = 1
    B = 2


def test_without_value_matcher():
    with pytest.raises(RCheckArgsError):
        RFullEnumKeyTypedDict()

    with pytest.raises(ValueError):
        RFullEnumKeyTypedDict(key_type=_AttrEnum, dictionary={})

    with pytest.raises(ValueError):
        RFullEnumKeyTypedDict(key_type=_AttrEnum, dictionary={_AttrEnum.A: "abc"})

    d = RFullEnumKeyTypedDict(key_type=_AttrEnum, dictionary={_AttrEnum.A: "abc", _AttrEnum.B: 123})

    d[_AttrEnum.B] = 456
    assert d[_AttrEnum.B] is 456

    with pytest.raises(AttributeError):
        del d[_AttrEnum.B]

    with pytest.raises(AttributeError):
        d.clear()


def test_with_value_matcher():
    with pytest.raises(ValueError):
        RFullEnumKeyTypedDict(key_type=_AttrEnum, value_matcher=INT, dictionary={})

    with pytest.raises(ValueError):
        RFullEnumKeyTypedDict(key_type=_AttrEnum, value_matcher=INT, dictionary={_AttrEnum.A: "abc"})

    with pytest.raises(RCheckArgsError):
        RFullEnumKeyTypedDict(key_type=_AttrEnum, value_matcher=INT, dictionary={_AttrEnum.A: "abc", _AttrEnum.B: 123})

    d = RFullEnumKeyTypedDict(key_type=_AttrEnum, value_matcher=INT, dictionary={_AttrEnum.A: 123, _AttrEnum.B: 456})

    with pytest.raises(RCheckArgsError):
        d[_AttrEnum.A] = "abc"

    d[_AttrEnum.A] = 789
    assert d[_AttrEnum.A] is 789
