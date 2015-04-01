from unittest import TestCase
from rambutan3.types.string.RNonEmptyText import RNonEmptyText


class TestRNonEmptyText(TestCase):

    def test(self):
        with self.assertRaises(TypeError):
            RNonEmptyText(None)
        with self.assertRaises(TypeError):
            RNonEmptyText(123)
        with self.assertRaises(ValueError):
            RNonEmptyText("")
        self.assertEqual("abc", RNonEmptyText("abc").str)
        self.assertEqual("abc  ", RNonEmptyText("abc  ").str)
        self.assertEqual("  abc  ", RNonEmptyText("  abc  ").str)
        self.assertEqual("  ", RNonEmptyText("  ").str)
