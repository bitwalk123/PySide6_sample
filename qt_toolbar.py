import sys

from PySide6.QtGui import QAction
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
        but_open.setText('Open')
        but_open.setToolTip('Open file to contents.')
        pixmap_open = QStyle.StandardPixmap.SP_DirOpenIcon
        icon_open = self.style().standardIcon(pixmap_open)
        but_open.setIcon(icon_open)
        but_open.clicked.connect(self.button_clicked)
        toolbar.addWidget(but_open)

        but_save = QToolButton()
        but_save.setText('Save')
        but_save.setToolTip('Save contents as file.')
        pixmap_save = QStyle.StandardPixmap.SP_DialogSaveButton
        icon_save = self.style().standardIcon(pixmap_save)
        but_save.setIcon(icon_save)
        but_save.clicked.connect(self.button_clicked)
        toolbar.addWidget(but_save)

        # spacer
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        toolbar.addWidget(spacer)

        but_exit = QToolButton()
        but_exit.setText('Exit')
        but_exit.setToolTip('Exit application.')
        pixmap_exit = QStyle.StandardPixmap.SP_BrowserStop
        icon_exit = self.style().standardIcon(pixmap_exit)
        but_exit.setIcon(icon_exit)
        but_exit.clicked.connect(self.button_clicked)
        toolbar.addWidget(but_exit)

    def button_clicked(self):
        obj: QToolButton = self.sender()
        print('%s button is clicked!' % obj.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
