import copy


class RDictWhereAtLeastMatcher(RDictMatcher):

    def __init__(self, value_matcher_map: dict):
        super().__init__(value_matcher_map)

    def matches(self, dict_: dict) -> bool:
        x = self._matches(dict_, is_exact=False)
        return x

    def _matches(self, dict_: dict, *, is_exact: bool) -> bool:
        if not super().matches(dict_):
            return False
        dict_copy = copy.deepcopy(dict_)
        """:type: dict"""
        for key, value_matcher in self.__value_matcher_map.items():
            value = dict_copy.get(key)
            if not value_matcher.matches(value):
                return False
            del dict_copy[key]
        if is_exact and dict_copy:
            return False
        return True


