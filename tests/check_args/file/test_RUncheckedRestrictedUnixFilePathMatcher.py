import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.file.RFilePathTypeEnum import RFilePathTypeEnum
from rambutan3.check_args.file.RUncheckedRestrictedUnixFilePathMatcher import RUncheckedRestrictedUnixFilePathMatcher


rel = [RFilePathTypeEnum.RELATIVE]
_abs = [RFilePathTypeEnum.ABSOLUTE]
rel_abs = [RFilePathTypeEnum.RELATIVE, RFilePathTypeEnum.ABSOLUTE]


def test_ctor():
    with pytest.raises(ValueError):
        RUncheckedRestrictedUnixFilePathMatcher()

    RUncheckedRestrictedUnixFilePathMatcher(*rel)
    RUncheckedRestrictedUnixFilePathMatcher(*_abs)
    RUncheckedRestrictedUnixFilePathMatcher(*rel_abs)

def test_check_arg():
    __check_arg(rel, '.', is_ok=True)
    __check_arg(rel_abs, '.', is_ok=True)
    __check_arg(_abs, '.', is_ok=False)
    __check_arg(rel, './', is_ok=True)
    __check_arg(rel, '..', is_ok=True)
    __check_arg(rel, '../', is_ok=True)
    __check_arg(rel, 'abc', is_ok=True)
    __check_arg(rel, 'abc/', is_ok=True)
    __check_arg(rel, '/abc/', is_ok=False)
    __check_arg(_abs, '/abc/', is_ok=True)
    __check_arg(rel_abs, '/abc/', is_ok=True)
    __check_arg(rel, '../abc/', is_ok=True)

    for p in ['abc//', 'abc^', 'abc$', 'abc%', r'abc\def', 'abc:def', 'abc def']:
        __check_arg(rel, p, is_ok=False)
        __check_arg(_abs, p, is_ok=False)
        __check_arg(rel_abs, p, is_ok=False)


def __check_arg(allowed_file_path_enum_iterable, path: str, *, is_ok: bool):
    m = RUncheckedRestrictedUnixFilePathMatcher(*allowed_file_path_enum_iterable)
    if is_ok:
        assert m.check_arg(path, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(path, 'dummy_arg_name')


def test__eq__and__ne__():
    RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*rel),
                             'abc',
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*rel),
                             RUncheckedRestrictedUnixFilePathMatcher(*rel),
                             is_equal=True)

    RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*rel),
                             RUncheckedRestrictedUnixFilePathMatcher(*_abs),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*rel),
                             RUncheckedRestrictedUnixFilePathMatcher(*rel_abs),
                             is_equal=False)

    RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*_abs),
                             RUncheckedRestrictedUnixFilePathMatcher(*rel_abs),
                             is_equal=False)

    for x in [rel, _abs, rel_abs]:
        RTestUtil.test_eq_ne_hash(RUncheckedRestrictedUnixFilePathMatcher(*x),
                                 RUncheckedRestrictedUnixFilePathMatcher(*x),
                                 is_equal=True)




def test__hash__():
    assert hash(RUncheckedRestrictedUnixFilePathMatcher(*rel)) != hash('abc')

    assert hash(RUncheckedRestrictedUnixFilePathMatcher(*rel)) \
           == \
           hash(RUncheckedRestrictedUnixFilePathMatcher(*rel))

    assert hash(RUncheckedRestrictedUnixFilePathMatcher(*rel)) \
           != \
           hash(RUncheckedRestrictedUnixFilePathMatcher(*_abs))

    assert hash(RUncheckedRestrictedUnixFilePathMatcher(*rel)) \
           != \
           hash(RUncheckedRestrictedUnixFilePathMatcher(*rel_abs))

    assert hash(RUncheckedRestrictedUnixFilePathMatcher(*_abs)) \
           != \
           hash(RUncheckedRestrictedUnixFilePathMatcher(*rel_abs))

    for x in [rel, _abs, rel_abs]:
        assert hash(RUncheckedRestrictedUnixFilePathMatcher(*x)) \
               == \
               hash(RUncheckedRestrictedUnixFilePathMatcher(*x))


def test__str__():
    assert str(RUncheckedRestrictedUnixFilePathMatcher(*rel)) \
           == 'str matching restricted UNIX file path pattern (RELATIVE)'
    assert str(RUncheckedRestrictedUnixFilePathMatcher(*_abs)) \
           == 'str matching restricted UNIX file path pattern (ABSOLUTE)'
    m = RUncheckedRestrictedUnixFilePathMatcher(*rel_abs)
    assert (str(m) == 'str matching restricted UNIX file path pattern (RELATIVE or ABSOLUTE)') \
    or (str(m) == 'str matching restricted UNIX file path pattern (ABSOLUTE or RELATIVE)')
