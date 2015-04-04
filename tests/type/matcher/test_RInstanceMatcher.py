from unittest import TestCase
from rambutan3.type.matcher.RInstanceMatcher import RInstanceMatcher


class X:
    pass


class TestRInstanceMatcher(TestCase):

    def test_ctor(self):
        with self.assertRaises(ValueError):
            RInstanceMatcher()
        with self.assertRaises(TypeError):
            RInstanceMatcher(None)
        with self.assertRaises(TypeError):
            RInstanceMatcher("abc")
        with self.assertRaises(TypeError):
            RInstanceMatcher(123)
        RInstanceMatcher(int)
        RInstanceMatcher(str)

    def test_matches(self):
        self.assertTrue(RInstanceMatcher(str).matches("abc"))
        self.assertFalse(RInstanceMatcher(str).matches(None))
        self.assertTrue(RInstanceMatcher(int).matches(123))
        self.assertFalse(RInstanceMatcher(int).matches(None))

    def test__eq__(self):
        self.assertFalse(RInstanceMatcher(str) == "abc")
        self.assertFalse("abc" == RInstanceMatcher(str))
        self.assertTrue(RInstanceMatcher(str) == RInstanceMatcher(str))
        self.assertTrue(RInstanceMatcher(int, str) == RInstanceMatcher(str, int))

    def test__str__(self):
        self.assertEqual(str(RInstanceMatcher(X)), X.__name__)
