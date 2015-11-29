from rambutan3.check_args.annotation.BUILTIN_DICT_WHERE_EXACTLY import BUILTIN_DICT_WHERE_EXACTLY
from tests.check_args.annotation import RDictMatcherTestUtil


def test():
    RDictMatcherTestUtil.core_test_dict_where_exactly_matcher(BUILTIN_DICT_WHERE_EXACTLY)
