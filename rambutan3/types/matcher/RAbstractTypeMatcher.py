"""Base classes for value matching

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""

from abc import abstractmethod

from rambutan3 import RArgs
from rambutan3.types.matcher.errfmt.RCheckArgsErrorFormatter import RCheckArgsErrorFormatter


class RCheckArgsError(Exception):
    """Raised by {@link RValueMatcher#check()}"""
    pass


RAbstractTypeMatcher = None
class RAbstractTypeMatcher:
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

    def contains(self, matcher: RAbstractTypeMatcher) -> bool:
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

        @throw TypeError
               if {@code matcher} is not type RValueMatcher
        """
        RArgs.check_is_instance(matcher, RAbstractTypeMatcher, "matcher")
        x = self._contains(matcher)
        return x

    @abstractmethod
    def _contains(self, matcher: RAbstractTypeMatcher) -> bool:
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

    def __or__(self, other: RAbstractTypeMatcher) -> RAbstractTypeMatcher:
        """operator|: Combines {@code self} with {@code other} to create logical OR value matcher

        @param other
               another value matcher

        @return new logical OR value matcher

        @see RLogicalOrValueMatcher
        """

        x = RLogicalOrTypeMatcher(self, other)
        return x

    def __str__(self):
        x = self._str()
        return x

    @abstractmethod
    def _str(self):
        """Called by {@link #__str__()}; abstract to force subclasses to override"""
        raise NotImplementedError()

RLogicalOrTypeMatcher = None
class RLogicalOrTypeMatcher(RAbstractTypeMatcher):
    """Combines two or more value matchers to create a unified logical OR value matcher"""

    def __init__(self,
                 left: (RAbstractTypeMatcher, RLogicalOrTypeMatcher),
                 right: (RAbstractTypeMatcher, RLogicalOrTypeMatcher)):
        """Never call this ctor directly; instead use operator|: {@link RValueMatcher#__or__()}

        @param left
               first value matcher; logical OR value matchers are handled correctly
        @param right
               second value matcher; logical OR value matchers are handled correctly

        @return new value matcher that combines first and second value matcher as logical OR value matcher
        """
        super().__init__()
        RArgs.check_is_instance(left, RAbstractTypeMatcher, "left")
        RArgs.check_is_instance(right, RAbstractTypeMatcher, "right")

        matcher_list = []
        if isinstance(left, RLogicalOrTypeMatcher):
            matcher_list.extend(left.__matcher_list)
        else:
            matcher_list.append(left)

        if isinstance(right, RLogicalOrTypeMatcher):
            matcher_list.extend(right.__matcher_list)
        else:
            matcher_list.append(right)

        #: :type: list of (RValueMatcher)
        self.__matcher_list = matcher_list

    # @override
    def matches(self, value) -> bool:
        # Ref: http://stackoverflow.com/q/5217489/257299
        x = any(y.matches(value) for y in self.__matcher_list)
        return x

    # @override
    def _contains(self, matcher: RAbstractTypeMatcher) -> bool:
        # Ref: http://stackoverflow.com/q/5217489/257299
        x = any(y.contains(matcher) for y in self.__matcher_list)
        return x

    def __iter__(self):
        """Iterates internal list of value matchers"""
        x = iter(self.__matcher_list)
        return x

    # @override
    def _str(self):
        x = " | ".join([str(x) for x in self.__matcher_list])
        return x
