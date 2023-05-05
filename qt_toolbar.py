import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget, QStyle,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('ToolBar')

    def initUI(self):
        # Create pyqt toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add buttons to toolbar
        but_open = QToolButton()
        pixmap_open = QStyle.StandardPixmap.SP_DirOpenIcon
        icon_open = self.style().standardIcon(pixmap_open)
        but_open.setIcon(icon_open)
        toolbar.addWidget(but_open)

        but_play = QToolButton()
        pixmap_play = QStyle.StandardPixmap.SP_MediaPlay
        icon_play = self.style().standardIcon(pixmap_play)
        but_play.setIcon(icon_play)
        toolbar.addWidget(but_play)

        # spacer
        spacer: QWidget = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        toolbar.addWidget(spacer)

        but_exit = QToolButton()
        but_exit.setIcon(QIcon.fromTheme('application-exit'))
        toolbar.addWidget(but_exit)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()