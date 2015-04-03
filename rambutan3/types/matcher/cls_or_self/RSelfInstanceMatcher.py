from rambutan3.types.matcher.cls_or_self.RAbstractClassOrSelfInstanceMatcher import RAbstractClassOrSelfInstanceMatcher


class RSelfInstanceMatcher(RAbstractClassOrSelfInstanceMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = isinstance(value, self._caller_class)
        return x

    # @override
    def _str(self):
        x = "self: {}".format(self._caller_class.__name__)
        return x
