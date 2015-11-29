from rambutan3.check_args.annotation.SET import SET
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_set_matcher(SET, set)
