from unittest import TestCase
from rambutan3.types.matcher.RValueMatcher import RValueMatcher, RLogicalOrValueMatcher


class _RValueMatcher(RValueMatcher):
    pass

class TestRLogicalOrValueMatcher(TestCase):

    def test_ctor(self):
        with self.assertRaises(TypeError):
            RLogicalOrValueMatcher(None, _RValueMatcher())
        with self.assertRaises(TypeError):
            RLogicalOrValueMatcher(_RValueMatcher(), None)
