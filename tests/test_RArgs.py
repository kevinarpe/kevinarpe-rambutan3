from unittest import TestCase
import RArgs


class TestRArgs(TestCase):

    def test_check_not_none(self):
        with self.assertRaises(ValueError):
            RArgs.check_not_none(None, "blah")
        self._test_check_not_none(123, "blah")
        self._test_check_not_none("abc", "blah")

    def _test_check_not_none(self, value, arg_name: str):
        result = RArgs.check_not_none(value, arg_name)
        self.assertEqual(value, result)

    def test_check_iterable_items_not_none(self):
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none(None, "blah")
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none((None,), "blah")
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none((123, None), "blah")
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none((123, None, 456), "blah")
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none(("abc", None), "blah")
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none((None, "abc"), "blah")
        self._test_check_iterable_items_not_none((), "blah")
        self._test_check_iterable_items_not_none((123,), "blah")
        self._test_check_iterable_items_not_none((123, "abc"), "blah")

    def _test_check_iterable_items_not_none(self, iterable, arg_name: str):
        result = RArgs.check_iterable_items_not_none(iterable, arg_name)
        self.assertEqual(iterable, result)
