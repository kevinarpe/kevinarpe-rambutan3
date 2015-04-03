from unittest import TestCase
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


class TestRInstanceMatcher(TestCase):

    def test_ctor(self):
        with self.assertRaises(TypeError):
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

    def test_contains(self):
        with self.assertRaises(TypeError):
            RInstanceMatcher(str).contains(None)
        with self.assertRaises(TypeError):
            RInstanceMatcher(str).contains("abc")
        self.assertTrue(RInstanceMatcher(_Superclass).contains(RInstanceMatcher(_Subclass)))
        self.assertFalse(RInstanceMatcher(_Subclass).contains(RInstanceMatcher(_Superclass)))

    def test_str(self):
        self.assertEqual(str(RInstanceMatcher(_Superclass)), _Superclass.__name__)
