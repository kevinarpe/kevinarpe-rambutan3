from rambutan3.check_args.annotation.BUILTIN_DICT_WHERE_AT_LEAST import BUILTIN_DICT_WHERE_AT_LEAST
from tests.check_args.annotation import RDictMatcherTestUtil


def test():
    RDictMatcherTestUtil.core_test_dict_where_at_least_matcher(BUILTIN_DICT_WHERE_AT_LEAST)
