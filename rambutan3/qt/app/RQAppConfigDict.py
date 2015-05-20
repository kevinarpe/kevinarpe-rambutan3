from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.container.RFullTypedEnumDict import RFullTypedEnumDict
from rambutan3.qt.app.RQAppConfigEnum import RQAppConfigEnum


class RQAppConfigDict(RFullTypedEnumDict):

    def __init__(self: SELF(), *, dictionary: DICT):
        super().__init__(key_type=RQAppConfigEnum, dictionary=dictionary)