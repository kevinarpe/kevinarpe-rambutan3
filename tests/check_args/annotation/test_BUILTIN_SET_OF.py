from rambutan3.check_args.annotation.BUILTIN_SET_OF import BUILTIN_SET_OF
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_set_of_matcher(BUILTIN_SET_OF)
