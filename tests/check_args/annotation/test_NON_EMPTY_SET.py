from rambutan3.check_args.annotation.NON_EMPTY_SET import NON_EMPTY_SET
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_non_empty_set_matcher(NON_EMPTY_SET, set)
