import pytest

from rambutan3 import RArgs


class _Superclass:
    pass


class _Subclass(_Superclass):
    pass


def test_check_not_none():
    _fail_check_not_none(None, "blah")
    _pass_check_not_none(123, "blah")
    _pass_check_not_none("abc", "blah")


def _fail_check_not_none(value, arg_name: str):
    with pytest.raises(ValueError):
        RArgs.check_not_none(value, arg_name)


def _pass_check_not_none(value, arg_name: str):
    result = RArgs.check_not_none(value, arg_name)
    assert value is result


class _Iterable:
    def __iter__(self):
        return self
    def __next__(self):
        return self


def test_check_is_iterable():
    _fail_check_is_iterable(None, "blah")
    # Special case: Do not allow str
    _fail_check_is_iterable("abc", "blah")
    _pass_check_is_iterable((), "blah")
    _pass_check_is_iterable((123,), "blah")
    _pass_check_is_iterable((123, 456), "blah")
    _pass_check_is_iterable([], "blah")
    _pass_check_is_iterable([123,], "blah")
    _pass_check_is_iterable([123, 456], "blah")
    _pass_check_is_iterable(_Iterable(), "blah")


def _fail_check_is_iterable(iterable, arg_name: str):
    with pytest.raises(TypeError):
        RArgs.check_is_iterable(iterable, arg_name)


def _pass_check_is_iterable(iterable, arg_name: str):
    result = RArgs.check_is_iterable(iterable, arg_name)
    assert iterable is result


def test_check_iterable_items_not_none():
    _fail_check_iterable_items_not_none(TypeError, None, "blah")
    _fail_check_iterable_items_not_none(ValueError, (None,), "blah")
    _fail_check_iterable_items_not_none(ValueError, (123, None), "blah")
    _fail_check_iterable_items_not_none(ValueError, (123, None, 456), "blah")
    _fail_check_iterable_items_not_none(ValueError, ("abc", None), "blah")
    _fail_check_iterable_items_not_none(ValueError, (None, "abc"), "blah")
    _pass_check_iterable_items_not_none((), "blah")
    _pass_check_iterable_items_not_none((123,), "blah")
    _pass_check_iterable_items_not_none((123, "abc"), "blah")


def _fail_check_iterable_items_not_none(exception_type: Exception, iterable, arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_iterable_items_not_none(iterable, arg_name)


def _pass_check_iterable_items_not_none(iterable, arg_name: str):
    result = RArgs.check_iterable_items_not_none(iterable, arg_name)
    assert iterable is result


def test_check_iterable_not_empty():
    _fail_check_iterable_not_empty(TypeError, None, "blah")
    _fail_check_iterable_not_empty(ValueError, (), "blah")
    _fail_check_iterable_not_empty(ValueError, tuple(), "blah")
    _fail_check_iterable_not_empty(ValueError, [], "blah")
    _fail_check_iterable_not_empty(ValueError, list(), "blah")
    _fail_check_iterable_not_empty(ValueError, {}, "blah")
    _fail_check_iterable_not_empty(ValueError, dict(), "blah")
    _fail_check_iterable_not_empty(ValueError, set(), "blah")
    _fail_check_iterable_not_empty(ValueError, frozenset(), "blah")
    _pass_check_iterable_not_empty((123,), "blah")
    _pass_check_iterable_not_empty(tuple([123]), "blah")
    _pass_check_iterable_not_empty([123], "blah")
    _pass_check_iterable_not_empty(list([123]), "blah")
    _pass_check_iterable_not_empty({123: "abc"}, "blah")
    _pass_check_iterable_not_empty(dict({123: "abc"}), "blah")
    _pass_check_iterable_not_empty({123}, "blah")
    _pass_check_iterable_not_empty(frozenset([123]), "blah")


def _fail_check_iterable_not_empty(exception_type: Exception, iterable, arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_iterable_not_empty(iterable, arg_name)


def _pass_check_iterable_not_empty(iterable, arg_name: str):
    result = RArgs.check_iterable_not_empty(iterable, arg_name)
    assert iterable is result


def test_check_iterable_not_empty_and_items_not_none():
    _fail_check_iterable_not_empty_and_items_not_none(TypeError, None, "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, (None,), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, (123, None), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, (123, None, 456), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, ("abc", None), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, (None, "abc"), "blah")
    _pass_check_iterable_not_empty_and_items_not_none((123,), "blah")
    _pass_check_iterable_not_empty_and_items_not_none((123, "abc"), "blah")

    _fail_check_iterable_not_empty_and_items_not_none(TypeError, None, "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, (), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, tuple(), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, [], "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, list(), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, {}, "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, dict(), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, set(), "blah")
    _fail_check_iterable_not_empty_and_items_not_none(ValueError, frozenset(), "blah")
    _pass_check_iterable_not_empty_and_items_not_none((123,), "blah")
    _pass_check_iterable_not_empty_and_items_not_none(tuple([123]), "blah")
    _pass_check_iterable_not_empty_and_items_not_none([123], "blah")
    _pass_check_iterable_not_empty_and_items_not_none(list([123]), "blah")
    _pass_check_iterable_not_empty_and_items_not_none({123: "abc"}, "blah")
    _pass_check_iterable_not_empty_and_items_not_none(dict({123: "abc"}), "blah")
    _pass_check_iterable_not_empty_and_items_not_none({123}, "blah")
    _pass_check_iterable_not_empty_and_items_not_none(frozenset([123]), "blah")


def _fail_check_iterable_not_empty_and_items_not_none(exception_type: Exception, iterable, arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_iterable_not_empty_and_items_not_none(iterable, arg_name)


def _pass_check_iterable_not_empty_and_items_not_none(iterable, arg_name: str):
    result = RArgs.check_iterable_not_empty_and_items_not_none(iterable, arg_name)
    assert iterable is result


def test_check_is_instance():
    _fail_check_is_instance(ValueError, 123, None, "blah")
    _fail_check_is_instance(TypeError, 123, "abc", "blah")
    _fail_check_is_instance(TypeError, 123, str, "blah")
    _fail_check_is_instance(TypeError, 123, (float, str), "blah")
    _fail_check_is_instance(TypeError, 123, (float, str), "blah{}", 8)
    _pass_check_is_instance(None, type(None), "blah")
    _pass_check_is_instance(None, (type(None),), "blah")
    _pass_check_is_instance(None, (type(None), str), "blah")
    _pass_check_is_instance(None, (str, type(None)), "blah")
    _pass_check_is_instance("abc", str, "blah")
    _pass_check_is_instance("abc", str, "blah", 8)
    _pass_check_is_instance("abc", (str, int), "blah", 8)
    _pass_check_is_instance("abc", (int, str), "blah", 8)


def _fail_check_is_instance(exception_type: Exception,
                            value, class_or_type_or_tuple_of, arg_name: str, *arg_name_format_args):
    with pytest.raises(exception_type):
        RArgs.check_is_instance(value, class_or_type_or_tuple_of, arg_name, *arg_name_format_args)


def _pass_check_is_instance(value, class_or_type_or_tuple_of, arg_name: str, *arg_name_format_args):
    result = RArgs.check_is_instance(value, class_or_type_or_tuple_of, arg_name, *arg_name_format_args)
    assert value is result


def test_check_iterable_items_is_instance():
    _fail_check_iterable_items_is_instance(TypeError, None, str, "blah")
    _fail_check_iterable_items_is_instance(TypeError, None, "abc", "blah")
    _pass_check_iterable_items_is_instance([], str, "blah")
    # _fail_check_iterable_items_is_instance(TypeError, [], "abc", "blah")
    _pass_check_iterable_items_is_instance(["abc"], str, "blah")
    _fail_check_iterable_items_is_instance(TypeError, ["abc"], "abc", "blah")
    _fail_check_iterable_items_is_instance(TypeError, ["abc", 123], str, "blah")


def _fail_check_iterable_items_is_instance(exception_type: Exception,
                                           iterable, class_or_type_or_tuple_of: (type, tuple), arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_iterable_items_is_instance(iterable, class_or_type_or_tuple_of, arg_name)


def _pass_check_iterable_items_is_instance(iterable, class_or_type_or_tuple_of: (type, tuple), arg_name: str):
    result = RArgs.check_iterable_items_is_instance(iterable, class_or_type_or_tuple_of, arg_name)
    assert iterable is result


def test_check_iterable_not_empty_and_items_is_instance():
    _fail_check_iterable_not_empty_and_items_is_instance(TypeError, None, str, "blah")
    _fail_check_iterable_not_empty_and_items_is_instance(TypeError, None, "abc", "blah")
    _fail_check_iterable_not_empty_and_items_is_instance(ValueError, [], str, "blah")
    _pass_check_iterable_not_empty_and_items_is_instance(["abc"], str, "blah")
    _fail_check_iterable_not_empty_and_items_is_instance(TypeError, ["abc"], "abc", "blah")
    _fail_check_iterable_not_empty_and_items_is_instance(TypeError, ["abc", 123], str, "blah")


def _fail_check_iterable_not_empty_and_items_is_instance(exception_type: Exception,
                                           iterable, class_or_type_or_tuple_of: (type, tuple), arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_iterable_not_empty_and_items_is_instance(iterable, class_or_type_or_tuple_of, arg_name)


def _pass_check_iterable_not_empty_and_items_is_instance(iterable, class_or_type_or_tuple_of: (type, tuple), arg_name: str):
    result = RArgs.check_iterable_not_empty_and_items_is_instance(iterable, class_or_type_or_tuple_of, arg_name)
    assert iterable is result


def test_check_is_subclass():
    _fail_check_is_subclass(TypeError, None, str, "blah")
    _fail_check_is_subclass(TypeError, None, None, "blah")
    _fail_check_is_subclass(TypeError, str, None, "blah")
    _fail_check_is_subclass(TypeError, _Superclass, _Subclass, "blah")
    _pass_check_is_subclass(str, str, "blah")
    _pass_check_is_subclass(_Superclass, _Superclass, "blah")
    _pass_check_is_subclass(_Subclass, _Superclass, "blah")


def _fail_check_is_subclass(exception_type: Exception,
                            subclass: type, superclass: type, subclass_arg_name: str):
    with pytest.raises(exception_type):
        RArgs.check_is_subclass(subclass, superclass, subclass_arg_name)


def _pass_check_is_subclass(subclass: type, superclass: type, subclass_arg_name: str):
    result = RArgs.check_is_subclass(subclass, superclass, subclass_arg_name)
    assert subclass is result
