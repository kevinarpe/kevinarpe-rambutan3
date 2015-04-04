from _collections_abc import Mapping, MutableMapping
from rambutan3.type.REnum import REnum


class RDictEnum(REnum):

    BUILTIN_DICT = (dict,)
    DICT = (dict, Mapping, MutableMapping)
