# from PySide.QtCore import QObject, QModelIndex, Qt
# from PySide.QtCore import QAbstractTableModel
from PyQt5.QtCore import QAbstractTableModel, QObject, QModelIndex, Qt, QVariant

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.ANY import ANY
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.container.RAbstractTable import RAbstractTable


class RQAbstractTableModel(QAbstractTableModel):

    @check_args
    def __init__(self: SELF(), parent: INSTANCE_OF(QObject) | NONE=None):
        super().__init__(parent)

    @check_args
    def flags(self: SELF(), index: INSTANCE_OF(QModelIndex)) -> INSTANCE_OF(Qt.ItemFlags):
        x = super().flags(index)
        return x


# QT_ITEM_DATA_ROLE = INSTANCE_OF(Qt.ItemDataRole) | INT
QT_ITEM_DATA_ROLE = INT


class RQTableModel(RQAbstractTableModel):
    """
    Ref: http://qt-project.org/doc/qt-4.8/model-view-programming.html#creating-new-models
    """

    @check_args
    def __init__(self: SELF(), table: INSTANCE_OF(RAbstractTable) | NONE=None):
        super().__init__()
        self.__table = table
        """:type: RAbstractTable"""

    # @overrides
    @check_args
    def data(self: SELF(), index: INSTANCE_OF(QModelIndex), role: QT_ITEM_DATA_ROLE=Qt.DisplayRole) -> ANY:
        """:type index: QModelIndex"""
        if not index.isValid():
            return None
        # TODO: Create enums?
        # elif Qt.ItemDataRole.DisplayRole != role:
        elif Qt.DisplayRole != role:
            return None
        else:
            x = self.__table.get_data(row_index=index.row(), column_index=index.column())
            return x

    @check_args
    def headerData(self: SELF(),
                   section: NON_NEGATIVE_INT,
                   orientation: INSTANCE_OF(Qt.Orientation),
                   role: QT_ITEM_DATA_ROLE=Qt.DisplayRole) -> ANY:
        if Qt.DisplayRole != role:
            # return None
            return QVariant()
        elif Qt.Horizontal == orientation:
            x = self.__table.get_header(column_index=section)
            # RMessageText does not work for PyQt.
            y = str(x)
            return y
        else:
            x = str(1 + section)
            return x

    def rowCount(self, parent: QModelIndex):
        return self.__table.row_count

    def columnCount(self, parent: QModelIndex):
        return self.__table.column_count
