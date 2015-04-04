from unittest import TestCase
import re
from rambutan3.type.string.RPatternText import RPatternText


class TestRPatternText(TestCase):

    __TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")

    def test(self):
        with self.assertRaises(TypeError):
            RPatternText(None, self.__TOKEN_PATTERN)
        with self.assertRaises(TypeError):
            RPatternText(123, self.__TOKEN_PATTERN)
        with self.assertRaises(ValueError):
            RPatternText("", self.__TOKEN_PATTERN)
        with self.assertRaises(ValueError):
            RPatternText("   ", self.__TOKEN_PATTERN)
        self.assertEqual("abc", RPatternText("abc", self.__TOKEN_PATTERN).str)
        self.assertEqual("abc_def", RPatternText("abc_def", self.__TOKEN_PATTERN).str)
