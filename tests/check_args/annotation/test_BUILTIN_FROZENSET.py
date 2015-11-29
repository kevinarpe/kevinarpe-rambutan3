from rambutan3.check_args.annotation.BUILTIN_FROZENSET import BUILTIN_FROZENSET
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_set_matcher(BUILTIN_FROZENSET, frozenset)
