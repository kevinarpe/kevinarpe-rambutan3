from rambutan3.check_args.annotation.BUILTIN_DICT_OF import BUILTIN_DICT_OF
from tests.check_args.annotation import RDictMatcherTestUtil


def test():
    RDictMatcherTestUtil.core_test_dict_of_matcher(BUILTIN_DICT_OF)
