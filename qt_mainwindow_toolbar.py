from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QToolBar, QStyle, QPushButton,
)

from qt_mainwindow_toolbutton import OpenToolButton


class MyToolBar(QToolBar):
    openClicked = Signal()

    def __init__(self):
        super().__init__()

        but_open = OpenToolButton()
        but_open.clicked.connect(self.on_clicked_open)
        self.addWidget(but_open)

    def on_clicked_open(self):
        self.openClicked.emit()
