# from PySide.QtGui import QTableView, QWidget
from PyQt5.QtWidgets import QTableView, QWidget
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.container.RRowTupleTable import RRowTupleTable
from rambutan3.qt.core.RQTableModel import RQTableModel
from rambutan3.string.RMessageText import RMessageText


class RQTableView(QTableView):

    @check_args
    def __init__(self: SELF(), parent: INSTANCE_OF(QWidget) | NONE=None):
        super().__init__(parent)

        header_list = [RMessageText('abc'), RMessageText('def'), RMessageText('ghi')]
        table = RRowTupleTable(header_list)
        table.append_row((1, 2, 3))
        table.append_row((10, 20, 30))
        table.append_row((100, 200, 300))
        table.append_row((1000, 2000, 3000))
        table.append_row((10000, 20000, 30000))
        table_model = RQTableModel(table)
        self.setModel(table_model)
        # self.setDropIndicatorShown(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
