from unittest import TestCase

from rambutan3 import RArgs


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


class TestRArgs(TestCase):

    def test_check_not_none(self):
        self._fail_check_not_none(None, "blah")
        self._pass_check_not_none(123, "blah")
        self._pass_check_not_none("abc", "blah")

    def _fail_check_not_none(self, value, arg_name: str):
        with self.assertRaises(ValueError):
            RArgs.check_not_none(value, arg_name)

    def _pass_check_not_none(self, value, arg_name: str):
        result = RArgs.check_not_none(value, arg_name)
        self.assertEqual(value, result)

    def test_check_iterable_items_not_none(self):
        self._fail_check_iterable_items_not_none(None, "blah")
        self._fail_check_iterable_items_not_none((None,), "blah")
        self._fail_check_iterable_items_not_none((123, None), "blah")
        self._fail_check_iterable_items_not_none((123, None, 456), "blah")
        self._fail_check_iterable_items_not_none(("abc", None), "blah")
        self._fail_check_iterable_items_not_none((None, "abc"), "blah")
        self._pass_check_iterable_items_not_none((), "blah")
        self._pass_check_iterable_items_not_none((123,), "blah")
        self._pass_check_iterable_items_not_none((123, "abc"), "blah")

    def _fail_check_iterable_items_not_none(self, iterable, arg_name: str):
        with self.assertRaises(ValueError):
            RArgs.check_iterable_items_not_none(iterable, arg_name)

    def _pass_check_iterable_items_not_none(self, iterable, arg_name: str):
        result = RArgs.check_iterable_items_not_none(iterable, arg_name)
        self.assertEqual(iterable, result)

    def test_check_iterable_not_empty(self):
        self._fail_check_iterable_not_empty(None, "blah")
        self._fail_check_iterable_not_empty((), "blah")
        self._fail_check_iterable_not_empty(tuple(), "blah")
        self._fail_check_iterable_not_empty([], "blah")
        self._fail_check_iterable_not_empty(list(), "blah")
        self._fail_check_iterable_not_empty({}, "blah")
        self._fail_check_iterable_not_empty(dict(), "blah")
        self._fail_check_iterable_not_empty(set(), "blah")
        self._fail_check_iterable_not_empty(frozenset(), "blah")
        self._pass_check_iterable_not_empty((123,), "blah")
        self._pass_check_iterable_not_empty(tuple([123]), "blah")
        self._pass_check_iterable_not_empty([123], "blah")
        self._pass_check_iterable_not_empty(list([123]), "blah")
        self._pass_check_iterable_not_empty({123: "abc"}, "blah")
        self._pass_check_iterable_not_empty(dict({123: "abc"}), "blah")
        self._pass_check_iterable_not_empty({123}, "blah")
        self._pass_check_iterable_not_empty(frozenset([123]), "blah")

    def _fail_check_iterable_not_empty(self, iterable, arg_name: str):
        with self.assertRaises(ValueError):
            RArgs.check_iterable_not_empty(iterable, arg_name)

    def _pass_check_iterable_not_empty(self, iterable, arg_name: str):
        result = RArgs.check_iterable_not_empty(iterable, arg_name)
        self.assertEqual(iterable, result)

    def test_check_iterable_not_empty_and_items_not_none(self):
        self._fail_check_iterable_not_empty_and_items_not_none(None, "blah")
        self._fail_check_iterable_not_empty_and_items_not_none((None,), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none((123, None), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none((123, None, 456), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(("abc", None), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none((None, "abc"), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none((123,), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none((123, "abc"), "blah")

        self._fail_check_iterable_not_empty_and_items_not_none(None, "blah")
        self._fail_check_iterable_not_empty_and_items_not_none((), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(tuple(), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none([], "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(list(), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none({}, "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(dict(), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(set(), "blah")
        self._fail_check_iterable_not_empty_and_items_not_none(frozenset(), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none((123,), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none(tuple([123]), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none([123], "blah")
        self._pass_check_iterable_not_empty_and_items_not_none(list([123]), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none({123: "abc"}, "blah")
        self._pass_check_iterable_not_empty_and_items_not_none(dict({123: "abc"}), "blah")
        self._pass_check_iterable_not_empty_and_items_not_none({123}, "blah")
        self._pass_check_iterable_not_empty_and_items_not_none(frozenset([123]), "blah")

    def _fail_check_iterable_not_empty_and_items_not_none(self, iterable, arg_name: str):
        with self.assertRaises(ValueError):
            RArgs.check_iterable_not_empty_and_items_not_none(iterable, arg_name)

    def _pass_check_iterable_not_empty_and_items_not_none(self, iterable, arg_name: str):
        result = RArgs.check_iterable_not_empty_and_items_not_none(iterable, arg_name)
        self.assertEqual(iterable, result)

    def test_check_is_instance(self):
        self._fail_check_is_instance(ValueError, 123, None, "blah")
        self._fail_check_is_instance(TypeError, 123, str, "blah")
        self._fail_check_is_instance(TypeError, 123, (float, str), "blah")
        self._fail_check_is_instance(TypeError, 123, (float, str), "blah{}", 8)
        self._pass_check_is_instance(None, type(None), "blah")
        self._pass_check_is_instance(None, (type(None),), "blah")
        self._pass_check_is_instance(None, (type(None), str), "blah")
        self._pass_check_is_instance(None, (str, type(None)), "blah")
        self._pass_check_is_instance("abc", str, "blah")
        self._pass_check_is_instance("abc", str, "blah", 8)
        self._pass_check_is_instance("abc", (str, int), "blah", 8)
        self._pass_check_is_instance("abc", (int, str), "blah", 8)

    def _fail_check_is_instance(self, exception_type: Exception,
                                value, class_or_type_or_tuple_of, arg_name: str, *arg_name_format_args):
        with self.assertRaises(exception_type):
            RArgs.check_is_instance(value, class_or_type_or_tuple_of, arg_name, *arg_name_format_args)

    def _pass_check_is_instance(self, value, class_or_type_or_tuple_of, arg_name: str, *arg_name_format_args):
        result = RArgs.check_is_instance(value, class_or_type_or_tuple_of, arg_name, *arg_name_format_args)
        self.assertEqual(value, result)

    def test_check_is_subclass(self):
        self._fail_check_is_subclass(ValueError, None, str, "blah")
        self._fail_check_is_subclass(ValueError, None, None, "blah")
        self._fail_check_is_subclass(ValueError, str, None, "blah")
        self._fail_check_is_subclass(TypeError, _Superclass, _Subclass, "blah")
        self._pass_check_is_subclass(str, str, "blah")
        self._pass_check_is_subclass(_Superclass, _Superclass, "blah")
        self._pass_check_is_subclass(_Subclass, _Superclass, "blah")

    def _fail_check_is_subclass(self, exception_type: Exception,
                                subclass: type, superclass: type, subclass_arg_name: str):
        with self.assertRaises(exception_type):
            RArgs.check_is_subclass(subclass, superclass, subclass_arg_name)

    def _pass_check_is_subclass(self, subclass: type, superclass: type, subclass_arg_name: str):
        result = RArgs.check_is_subclass(subclass, superclass, subclass_arg_name)
        self.assertEqual(subclass, result)
