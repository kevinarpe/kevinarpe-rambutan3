from _collections_abc import Mapping, MutableMapping
from rambutan3.types.REnum import REnum


class RDictEnum(REnum):

    BUILTIN_DICT = (dict,)
    DICT = (dict, Mapping, MutableMapping)
