from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QToolBar,
)

from qt_mainwindow_toolbutton import OpenToolButton


class MyToolBar(QToolBar):
    openClicked = Signal()

    def __init__(self):
        super().__init__()

        but_open = OpenToolButton()
        but_open.clicked.connect(self.on_clicked_open)
        self.addWidget(but_open)
        lab = QLabel("ToolBar")
        lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.addWidget(lab)


    def on_clicked_open(self):
        self.openClicked.emit()
