from unittest import TestCase
from rambutan3.type.string.RNonEmptyStr import RNonEmptyStr


class TestRNonEmptyText(TestCase):

    def test(self):
        with self.assertRaises(TypeError):
            RNonEmptyStr(None)
        with self.assertRaises(TypeError):
            RNonEmptyStr(123)
        with self.assertRaises(ValueError):
            RNonEmptyStr("")
        self.assertEqual("abc", RNonEmptyStr("abc").str)
        self.assertEqual("abc  ", RNonEmptyStr("abc  ").str)
        self.assertEqual("  abc  ", RNonEmptyStr("  abc  ").str)
        self.assertEqual("  ", RNonEmptyStr("  ").str)
