from abc import abstractmethod, ABC
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE import TYPE
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER
from rambutan3.check_args.annotation.IDENTIFIER import IDENTIFIER
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.error.RTypeMatcherErrorFormatter import RTypeMatcherErrorFormatter
from rambutan3.string.RIdentifier import RIdentifier


class RProperty(ABC):
    """
    Type vs Class: http://stackoverflow.com/a/4162594/257299
    """

    __ERROR_FORMATTER = RTypeMatcherErrorFormatter()
    __SENTINEL = object()
    __DEFAULT_VALUE_ATTR_NAME = "__default_value"

    @check_args
    def __init__(self: SELF(),
                 *,
                 owner_class: TYPE,
                 name: IDENTIFIER,
                 value_matcher: TYPE_MATCHER,
                 is_optional: BOOL,
                 can_read: BOOL,
                 can_write: BOOL):
        self.__owner_class = owner_class
        self.__owner_type_matcher = INSTANCE_OF(owner_class)
        self.__name = name
        self.__value_matcher = value_matcher
        self.__is_optional = is_optional
        self.__can_read = can_read
        self.__can_write = can_write

    @property
    def owner_class(self) -> type:
        return self.__owner_class

    @property
    def owner_type_matcher(self) -> RInstanceMatcher:
        return self.__owner_type_matcher

    @property
    def name(self) -> RIdentifier:
        return self.__name

    @property
    def value_matcher(self) -> type:
        return self.__value_matcher

    @property
    def is_optional(self) -> bool:
        return self.__is_optional

    @property
    def can_read(self) -> bool:
        return self.__can_read

    @property
    def default_value(self):
        x = getattr(self.__dict__, self.__DEFAULT_VALUE_ATTR_NAME, self.__SENTINEL)

        if x is self.__SENTINEL:
            x = self._default_value
            self.__value_matcher.check(x, self.__ERROR_FORMATTER,
                                       "Default value for property {}.{}: ", self.__owner_class.__name__, self.__name)
            setattr(self, self.__DEFAULT_VALUE_ATTR_NAME, x)

        return x

    @property
    @abstractmethod
    def _default_value(self):
        """Some default values cannot be obtained at start of Python, due to order of initialisation with external
        libraries -- PySide / Qt.  Delay the lookup using this abstract property.
        """
        raise NotImplementedError()

    @property
    def can_write(self) -> bool:
        return self.__can_write

    def get(self, owner):
        if not self.can_read:
            raise NotImplementedError("Property {}.{} is not readable"
                                      .format(self.__owner_class.__name__, self.__name))
        self.__owner_type_matcher.check(owner, self.__ERROR_FORMATTER, "Property {}.{}: Argument 'owner': ",
                                        self.__owner_class.__name__, self.__name)
        x = self._get(owner)
        return x

    def _get(self, owner):
        raise NotImplementedError()

    def set(self, owner, value):
        if not self.can_write:
            raise NotImplementedError("Property {}.{} is not writable"
                                      .format(self.__owner_class.__name__, self.__name))
        self.__owner_type_matcher.check(owner, self.__ERROR_FORMATTER, "Property {}.{}: Argument 'owner': ",
                                        self.__owner_class.__name__, self.__name)
        self.__value_matcher.check(value, self.__ERROR_FORMATTER, "Property {}.{}: Argument 'value': ",
                                   self.__owner_class.__name__, self.__name)
        self._set(owner, value)

    def _set(self, owner, value):
        raise NotImplementedError()

    # TODO: LAST: Builder shall accept enums for each top-most superclass, down to most subclass.
    # Items like 'modal' or 'minimumSize' can overwrite.  Use fixed size dict.
    # We need properties b/c PySide has weakly typed interfaces to the C++.
