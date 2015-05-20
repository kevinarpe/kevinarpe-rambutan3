# from PySide.QtCore import Slot, QObject
# from PySide.QtGui import QMainWindow
# from PySide.QtGui import QAction
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF


class RQActionExit(QAction):

    @check_args
    def __init__(self: SELF(), parent: INSTANCE_OF(QMainWindow)):
        super().__init__("E&xit", parent)
        self.triggered.connect(self.__slot_triggered)

    @pyqtSlot()
    def __slot_triggered(self):
        self.parentWidget().close()
