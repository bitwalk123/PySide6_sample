from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QStyle,
    QToolBar,
    QToolButton,
    QWidget,
)


def get_icon(parent: QWidget, name: str) -> QIcon:
    pixmap = getattr(QStyle.StandardPixmap, name)
    icon = parent.style().standardIcon(pixmap)
    return icon


class MyToolBar(QToolBar):
    playVideo = Signal()
    readVideo = Signal(str)

    def __init__(self):
        super().__init__()
        # Ioen
        but_open = QToolButton()
        but_open.setIcon(get_icon(self, 'SP_DirIcon'))
        but_open.clicked.connect(self.on_clicked_open)
        self.addWidget(but_open)
        # Play
        but_play = QToolButton()
        but_play.setIcon(get_icon(self, 'SP_MediaPlay'))
        but_play.clicked.connect(self.on_clicked_play)
        self.addWidget(but_play)

    def on_clicked_open(self):
        dialog = QFileDialog()
        dialog.setWindowTitle('Open video file')
        dialog.setNameFilter('Video (*.mp4)')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.readVideo.emit(filename)

    def on_clicked_play(self):
        self.playVideo.emit()
