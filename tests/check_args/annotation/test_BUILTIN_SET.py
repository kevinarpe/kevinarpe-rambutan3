from rambutan3.check_args.annotation.BUILTIN_SET import BUILTIN_SET
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_set_matcher(BUILTIN_SET, set)
