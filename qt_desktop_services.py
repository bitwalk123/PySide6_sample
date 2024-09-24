import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
    QToolBar,
    QToolButton,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = QUrl('https://doc.qt.io/qtforpython-6/')
        self.setWindowTitle('open URL')

        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        but = QToolButton()
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMenuButton
        )
        but.setIcon(icon)
        but.clicked.connect(self.on_click)
        toolbar.addWidget(but)

    def on_click(self):
        QDesktopServices.openUrl(self.url)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
