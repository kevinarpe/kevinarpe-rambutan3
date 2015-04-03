from unittest import TestCase
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher, RLogicalOrTypeMatcher


_INT_MATCHER = RInstanceMatcher(int)
_STR_MATCHER = RInstanceMatcher(str)


class TestRLogicalOrValueMatcher(TestCase):

    def test_ctor(self):
        with self.assertRaises(TypeError):
            RLogicalOrTypeMatcher()
        with self.assertRaises(TypeError):
            RLogicalOrTypeMatcher(None)
        with self.assertRaises(TypeError):
            RLogicalOrTypeMatcher(None, _STR_MATCHER)
        with self.assertRaises(TypeError):
            RLogicalOrTypeMatcher(_INT_MATCHER, None)
        RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)

    def test_matches(self):
        matcher = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
        self.assertTrue(matcher.matches("abc"))
        self.assertTrue(matcher.matches(123))
        self.assertFalse(matcher.matches(None))
        self.assertFalse(matcher.matches(123.456))

    def test_contains(self):
        TODO

    def test_iter(self):
        matcher = RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)
        it = iter(matcher)
        self.assertIs(_INT_MATCHER, next(it))
        self.assertIs(_STR_MATCHER, next(it))
        with self.assertRaises(StopIteration):
            next(it)

    def test_str(self):
        self.assertEqual("int | str", str(RLogicalOrTypeMatcher(_INT_MATCHER, _STR_MATCHER)))
