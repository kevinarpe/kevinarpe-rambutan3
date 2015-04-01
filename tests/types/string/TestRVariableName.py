from unittest import TestCase
import re
from rambutan3.types.string.RVariableName import RVariableName


class TestRVariableName(TestCase):

    __TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")

    def test(self):
        with self.assertRaises(TypeError):
            RVariableName(None)
        with self.assertRaises(TypeError):
            RVariableName(123)
        with self.assertRaises(ValueError):
            RVariableName("")
        with self.assertRaises(ValueError):
            RVariableName("   ")
        self.assertEqual("abc", RVariableName("abc").str)
        self.assertEqual("abc_def", RVariableName("abc_def").str)
