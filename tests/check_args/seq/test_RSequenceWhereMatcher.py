import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceWhereMatcher import RSequenceWhereMatcher


def test_ctor():
    with pytest.raises(TypeError):
        RSequenceWhereMatcher()

    RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True)
    RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=False)

    with pytest.raises(TypeError):
        RSequenceWhereMatcher("abc", [INT], is_exact=True)

    with pytest.raises(TypeError):
        RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, "abc", is_exact=True)

    with pytest.raises(TypeError):
        RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, ["abc"], is_exact=True)

    with pytest.raises(TypeError):
        RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=1)

    with pytest.raises(TypeError):
        RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact="abc")

    with pytest.raises(TypeError):
        RSequenceWhereMatcher("abc", 123, is_exact=456.789)


def test_check_arg():
    __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], [123, "abc", 456.789], is_exact=True)
    __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], [123, "abc", 456.789, True], is_exact=False)

    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], "non_sequence", is_exact=True)

    # Too short
    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], ["abc", "abc"], is_exact=True)

    # Too short
    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], ["abc", "abc"], is_exact=False)

    # Bad 2nd type
    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], ["abc", "abc", 456.789], is_exact=True)

    # Bad 2nd type
    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], ["abc", "abc", 456.789], is_exact=False)

    # Too long
    with pytest.raises(RCheckArgsError):
        __check_arg(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], [123, "abc", 456.789, "def"], is_exact=True)


def __check_arg(seq_enum: RSequenceEnum, element_matcher_seq, value, *, is_exact: bool):
    m = RSequenceWhereMatcher(seq_enum, element_matcher_seq, is_exact=is_exact)
    assert value is m.check_arg(value, 'dummy_arg_name')


def test__or__():
    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, [123, "abc", 456.789],
         is_exact=True,
         is_exception_expected=False)

    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, [123, "abc", 456.789, True],
         is_exact=False,
         is_exception_expected=False)

    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, 123,
         is_exact=True,
         is_exception_expected=False)

    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, 123,
         is_exact=False,
         is_exception_expected=False)

    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, 123.456,
         is_exact=True,
         is_exception_expected=True)

    __or(RSequenceEnum.SEQUENCE, [INT, STR, FLOAT], INT, 123.456,
         is_exact=False,
         is_exception_expected=True)


def __or(seq_enum: RSequenceEnum,
         element_matcher_seq,
         other_matcher: RAbstractTypeMatcher,
         value,
         *,
         is_exact: bool,
         is_exception_expected: bool):

    m = RSequenceWhereMatcher(seq_enum, element_matcher_seq, is_exact=is_exact)

    m2 = m | other_matcher

    if is_exception_expected:
        with pytest.raises(RCheckArgsError):
            assert value is m2.check_arg(value, 'dummy_arg_name')
    else:
        assert value is m2.check_arg(value, 'dummy_arg_name')

    m3 = other_matcher | m

    if is_exception_expected:
        with pytest.raises(RCheckArgsError):
            assert value is m3.check_arg(value, 'dummy_arg_name')
    else:
        assert value is m3.check_arg(value, 'dummy_arg_name')


def test__eq__and__ne__():
    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             'abc',
                             is_equal=False)

    RTestUtil.test_eq_ne_hash('abc',
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.TUPLE, [INT], is_exact=True),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=False),
                             RSequenceWhereMatcher(RSequenceEnum.TUPLE, [INT], is_exact=False),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             is_equal=True)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=False),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=False),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT], is_exact=True),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=True),
                             is_equal=True)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=False),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=False),
                             is_equal=True)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [STR, INT], is_exact=True),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=False),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [STR, INT], is_exact=False),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=True),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=False),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=False),
                             RSequenceWhereMatcher(RSequenceEnum.SEQUENCE, [INT, STR], is_exact=True),
                             is_equal=False)

def test__str__():
    assert str(RSequenceWhereMatcher(RSequenceEnum.TUPLE, [INT], is_exact=True)) == 'tuple where EXACTLY (int)'
    assert str(RSequenceWhereMatcher(RSequenceEnum.TUPLE, [INT, STR], is_exact=True)) == 'tuple where EXACTLY (int, str)'
    assert str(RSequenceWhereMatcher(RSequenceEnum.TUPLE, [STR, INT], is_exact=True)) == 'tuple where EXACTLY (str, int)'
