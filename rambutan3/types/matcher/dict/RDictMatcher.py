from rambutan3 import RArgs
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.types.matcher.dict.RDictEnum import RDictEnum


class RDictMatcher(RInstanceMatcher):

    def __init__(self, dict_enum: RDictEnum):
        RArgs.check_is_instance(dict_enum, RDictEnum, "dict_enum")
        super().__init__(*(dict_enum.value))
