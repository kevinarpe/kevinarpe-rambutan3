import pytest

from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceMatcher import RUniqueSequenceMatcher


def test_check_arg():
    __check_arg(RSequenceEnum.LIST, [], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, {}, "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, [123, 123, 456, 789], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, [123, 456, 123, 789], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, [123, 456, 123, 789, 123, 123], "a_list")


def __check_arg(seq_enum: RSequenceEnum, value, arg_name: str, *arg_name_format_args):
    m = RUniqueSequenceMatcher(seq_enum)
    assert value is m.check_arg(value, arg_name, *arg_name_format_args)


def test__str__():
    m = RUniqueSequenceMatcher(RSequenceEnum.LIST)
    assert 'unique list' == str(m)
