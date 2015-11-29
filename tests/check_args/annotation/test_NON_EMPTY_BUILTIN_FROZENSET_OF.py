from rambutan3.check_args.annotation.NON_EMPTY_BUILTIN_FROZENSET_OF import NON_EMPTY_BUILTIN_FROZENSET_OF
from tests.check_args.annotation import RSetMatcherTestUtil


def test():
    RSetMatcherTestUtil.core_test_non_empty_set_of_matcher(NON_EMPTY_BUILTIN_FROZENSET_OF, frozenset)
