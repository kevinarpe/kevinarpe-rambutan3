"""Base classes for value matching

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""

from abc import abstractmethod

from rambutan3 import RArgs
from rambutan3.types.matcher.errfmt.RCheckArgsErrorFormatter import RCheckArgsErrorFormatter


class RCheckArgsError(Exception):
    """Raised by {@link RValueMatcher#check()}"""
    pass


RValueMatcher = None
class RValueMatcher:
    """Abstract base class for all value matchers, include type matchers."""

    @abstractmethod
    def matches(self, value) -> bool:
        """Tests if value matches

        Example: if matcher requires an instance of type {@code str}, then {@code "abc"} will return {@code True}.

        @param value
               value to test / match / check

        @return {@code True} if value matches, else {@code False}
        """
        raise NotImplementedError()

    @abstractmethod
    def contains(self, matcher: RValueMatcher) -> bool:
        """Tests if another matcher is contained by this matcher ({@code self})

        Example:
        class Superclass: pass
        class Subclass(Superclass): pass
        superclass_matcher = RInstanceMatcher(Superclass)
        subclass_matcher = RInstanceMatcher(Subclass)
        assertTrue(superclass_matcher.contains(subclass_matcher))
        assertFalse(subclass_matcher.contains(superclass_matcher))

        @param matcher
               another matcher to test if contained by this matcher

        @return {@code True} if {@code self} can be substituted for {@code matcher}
        """
        raise NotImplementedError()

    def check(self,
              value,
              error_formatter: RCheckArgsErrorFormatter=RCheckArgsErrorFormatter(),
              *args,
              **kwargs):
        """Checks if a value matches this matcher ({@code self})

        @param value
               value to test
        @param error_formatter (optional: RCheckArgsErrorFormatter)
               generates an exception message if test fails
        @param *args
               passed directly to {@code error_formatter.format()}
        @param **kwargs
               passed directly to {@code error_formatter.format()}

        @throws RCheckArgsError
                if test fails
        """
        if not self.matches(value):
            x = error_formatter.format(self, value, *args, **kwargs)
            raise RCheckArgsError(x)

    def __or__(self, other: RValueMatcher) -> RValueMatcher:
        """operator|: Combines {@code self} with {@code other} to create logical OR value matcher

        @param other
               another value matcher

        @return new logical OR value matcher

        @see RLogicalOrValueMatcher
        """

        x = RLogicalOrValueMatcher(self, other)
        return x

    @abstractmethod
    def _str(self):
        """Called by {@link #__str__()}; abstract to force subclasses to override"""
        raise NotImplementedError()

    def __str__(self):
        x = self._str()
        return x

RLogicalOrValueMatcher = None
class RLogicalOrValueMatcher(RValueMatcher):
    """Combines two or more value matchers to create a unified logical OR value matcher"""

    def __init__(self, left: (RValueMatcher, RLogicalOrValueMatcher), right: (RValueMatcher, RLogicalOrValueMatcher)):
        """Never call this ctor directly; instead use operator|: {@link RValueMatcher#__or__()}

        @param left
               first value matcher; logical OR value matchers are handled correctly
        @param right
               second value matcher; logical OR value matchers are handled correctly

        @return new value matcher that combines first and second value matcher as logical OR value matcher
        """
        super().__init__()
        RArgs.check_is_instance(left, RValueMatcher, "left")
        RArgs.check_is_instance(right, RValueMatcher, "right")

        L = []
        if isinstance(left, RLogicalOrValueMatcher):
            L.extend(left.__list)
        else:
            L.append(left)
        if isinstance(right, RLogicalOrValueMatcher):
            L.extend(right.__list)
        else:
            L.append(right)

        #: :type: list of (RValueMatcher)
        self.__list = L

    def matches(self, value) -> bool:
        # Ref: http://stackoverflow.com/q/5217489/257299
        x = any(y.matches(value) for y in self.__list)
        return x

    def contains(self, matcher: RValueMatcher) -> bool:
        # Ref: http://stackoverflow.com/q/5217489/257299
        x = any(y.contains(matcher) for y in self.__list)
        return x

    def __iter__(self):
        """Iterates internal list of value matchers"""
        x = iter(self.__list)
        return x

    def _str(self):
        x = " | ".join([str(x) for x in self.__list])
        return x
