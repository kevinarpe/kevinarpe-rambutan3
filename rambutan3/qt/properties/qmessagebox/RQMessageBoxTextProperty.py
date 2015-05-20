from rambutan3.RProperty import RProperty
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.IDENTIFIER import IDENTIFIER
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE import TYPE
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


class RQMessageBoxTextProperty(RProperty):

    def __init__(self):
        super().__init__(owner_class=QMessageBox,
                         name=name,
                         value_matcher=value_matcher,
                         is_optional=is_optional,
                         can_read=can_read,
                         can_write=can_write)