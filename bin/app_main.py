import sys

# from PySide.QtGui import QApplication
from PyQt5.QtWidgets import QApplication

from rambutan3.qt.app.RQAppConfigDict import RQAppConfigDict
from rambutan3.qt.app.RQAppConfigEnum import RQAppConfigEnum
from rambutan3.qt.gui.RQAppQMainWindow import RQAppQMainWindow
from rambutan3.string.RMessageText import RMessageText


def main():
    # Available later from global variable QtGui.qApp
    app = QApplication(sys.argv)
    app_config_dict = \
        RQAppConfigDict(dictionary={RQAppConfigEnum.MESSAGE_BOX_WINDOW_TITLE: RMessageText("Rambutan Data Explorer")})
    widget = RQAppQMainWindow(app_config_dict=app_config_dict)
    widget.show()
    status = app.exec_()
    sys.exit(status)


if __name__ == "__main__":
    main()
