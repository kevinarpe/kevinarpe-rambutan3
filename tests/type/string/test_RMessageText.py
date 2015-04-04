from unittest import TestCase
from rambutan3.type.string.RMessageText import RMessageText


class TestRMessageText(TestCase):

    def test(self):
        with self.assertRaises(TypeError):
            RMessageText(None)
        with self.assertRaises(TypeError):
            RMessageText(123)
        with self.assertRaises(ValueError):
            RMessageText("")
        with self.assertRaises(ValueError):
            RMessageText("   ")
        self.assertEqual("abc", RMessageText("abc").str)
        self.assertEqual("abc  ", RMessageText("abc  ").str)
        self.assertEqual("  abc  ", RMessageText("  abc  ").str)
