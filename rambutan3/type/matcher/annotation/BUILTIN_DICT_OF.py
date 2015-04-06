from rambutan3.type.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.type.matcher.dict.RDictEnum import RDictEnum
from rambutan3.type.matcher.dict.RDictOfMatcher import RDictOfMatcher
from rambutan3.type.matcher.dict.RDictWhereMatcher import RDictWhereMatcher


def BUILTIN_DICT_OF(*,
                    key_matcher: RAbstractTypeMatcher=None,
                    value_matcher: RAbstractTypeMatcher=None) \
        -> RDictOfMatcher:
    x = RDictOfMatcher(RDictEnum.BUILTIN_DICT, key_matcher=key_matcher, value_matcher=value_matcher)
    return x