# from PySide.QtCore import Qt
# from PySide.QtGui import QMainWindow, QWidget, QCloseEvent, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.qt.app.RQAppConfigDict import RQAppConfigDict
from rambutan3.qt.app.RQAppConfigEnum import RQAppConfigEnum
from rambutan3.qt.gui.RQActionExit import RQActionExit
from rambutan3.qt.gui.RQTableView import RQTableView


class RQAppQCloseEventHandler:

    @check_args
    def __init__(self: SELF(), app_config_dict: INSTANCE_OF(RQAppConfigDict)):
        super().__init__()
        self.__message_box = QMessageBox()
        window_title = app_config_dict[RQAppConfigEnum.MESSAGE_BOX_WINDOW_TITLE]
        self.__message_box.setWindowTitle(window_title)
        self.__message_box.setIcon(QMessageBox.Question)
        self.__message_box.setText("Close all windows and exit?")
        self.__message_box.setInformativeText("All settings are saved automatically.")
        self.__message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.__message_box.setDefaultButton(QMessageBox.Ok)
        self.__message_box.setEscapeButton(QMessageBox.Cancel)
        self.__message_box.setWindowModality(Qt.ApplicationModal)

    @check_args
    def closeEvent(self: SELF(), event: INSTANCE_OF(QCloseEvent)):
        # Reset the default button if the message box has been used previously and cancel was clicked.
        self.__message_box.setDefaultButton(QMessageBox.Ok)
        result = self.__message_box.exec_()
        is_accept = (result == QMessageBox.Ok)
        event.setAccepted(is_accept)


# TODO: Create app config that saves automagically all the time.
# Example: Window position and size

class RQAppQMainWindow(QMainWindow):

    @check_args
    def __init__(self: SELF(),
                 *,
                 app_config_dict: INSTANCE_OF(RQAppConfigDict),
                 parent: INSTANCE_OF(QWidget) | NONE=None,
                 flags: INSTANCE_OF(Qt.WindowFlags)=Qt.WindowFlags(0)):
        super().__init__(parent, flags)

        window_title = app_config_dict[RQAppConfigEnum.MESSAGE_BOX_WINDOW_TITLE]
        self.setWindowTitle(window_title)

        # Nice starting size, but not a min or max.
        self.resize(1024, 768)
        # Any smaller and it is probably a mistake.  Those weird tiny resized windows @ 64x32 drive me crazy.
        self.setMinimumSize(160, 120)

        table_view = RQTableView(parent=self)
        self.setCentralWidget(table_view)

        # Create a status bar owned by self
        status_bar = self.statusBar()
        """:type: QStatusBar"""
        status_bar.setSizeGripEnabled(True)

        # Create a menu bar owned by self
        menu_bar = self.menuBar()
        """:type: QMenuBar"""
        file_menu = menu_bar.addMenu("&File")
        """:type: QMenu"""
        file_menu.addAction(RQActionExit(self))

        self.__close_event_handler = RQAppQCloseEventHandler(app_config_dict)

    @check_args
    def closeEvent(self: SELF(), event: INSTANCE_OF(QCloseEvent)):
        self.__close_event_handler.closeEvent(event)
