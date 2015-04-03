from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.dict.RDictEnum import RDictEnum
from rambutan3.types.matcher.dict.RDictMatcher import RDictMatcher


class RDictOfMatcher(RDictMatcher):

    def __init__(self, dict_enum: RDictEnum, *,
                 key_matcher: RAbstractTypeMatcher=None,
                 value_matcher: RAbstractTypeMatcher=None):
        super().__init__(dict_enum)
        self.check_init_args(key_matcher=key_matcher, value_matcher=value_matcher)
        self.__key_matcher = key_matcher
        self.__value_matcher = value_matcher

    # @override
    def matches(self, d: dict) -> bool:
        if not super().matches(d):
            return False
        x = self.core_matches(d, key_matcher=self.__key_matcher, value_matcher=self.__value_matcher)
        return x

    # @override
    def _str(self):
        x = self.core_str(super()._str(), key_matcher=self.__key_matcher, value_matcher=self.__value_matcher)
        return x

    @classmethod
    def check_init_args(cls, *,
                        key_matcher: RAbstractTypeMatcher=None,
                        value_matcher: RAbstractTypeMatcher=None):
        if key_matcher is None and value_matcher is None:
            raise ValueError("Both args 'key_matcher' and 'value_matcher' are None")

        if key_matcher is not None:
            RArgs.check_is_instance(key_matcher, RAbstractTypeMatcher, "key_matcher")

        if value_matcher is not None:
            RArgs.check_is_instance(value_matcher, RAbstractTypeMatcher, "value_matcher")

    @classmethod
    def core_matches(cls, d: dict, *,
                     key_matcher: RAbstractTypeMatcher=None,
                     value_matcher: RAbstractTypeMatcher=None):
        if key_matcher:
            for key in d.keys():
                if not key_matcher.matches(key):
                    return False

        if value_matcher:
            for value in d.values():
                if not value_matcher.matches(value):
                    return False

    @classmethod
    def core_str(cls, super_str: str, *,
                 key_matcher: RAbstractTypeMatcher=None,
                 value_matcher: RAbstractTypeMatcher=None):
        m = ""

        if key_matcher:
            m = "keys: {}".format(key_matcher)

        if value_matcher:
            if m:
                m += ", "
            m += "values: {}".format(value_matcher)

        x = "{} of [{}]".format(super_str, m)
        return x
