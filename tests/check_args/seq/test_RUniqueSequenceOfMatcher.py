import pytest

from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RUniqueSequenceOfMatcher import RUniqueSequenceOfMatcher


def test_check_arg():
    __check_arg(RSequenceEnum.LIST, INT, [], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, INT, {}, "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, INT, [123, 'abc'], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, INT, [123, 123, 456, 789], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, INT, [123, 456, 123, 789], "a_list")

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.LIST, INT, [123, 456, 123, 789, 123, 123], "a_list")


def __check_arg(seq_enum: RSequenceEnum,
                element_matcher: RAbstractTypeMatcher,
                value,
                arg_name: str,
                *arg_name_format_args):
    m = RUniqueSequenceOfMatcher(seq_enum, element_matcher)
    assert value is m.check_arg(value, arg_name, *arg_name_format_args)


def test__eq__():
    assert not RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT) == "abc"
    assert not "abc" == RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT)
    assert RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT) == RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT)
    assert RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT | FLOAT) == RUniqueSequenceOfMatcher(RSequenceEnum.LIST, FLOAT | INT)


def test__hash__():
    assert hash(RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT)) == hash(RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT))
    assert hash(RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT | FLOAT)) == hash(RUniqueSequenceOfMatcher(RSequenceEnum.LIST, FLOAT | INT))


def test__str__():
    m = RUniqueSequenceOfMatcher(RSequenceEnum.LIST, INT)
    assert 'unique list of [int]' == str(m)
