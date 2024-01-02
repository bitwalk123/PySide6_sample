# Reference:
# https://www.pythonguis.com/tutorials/pyside6-actions-toolbars-menus/
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menubar')
        self.init_ui()

    def init_ui(self):
        # Menubar
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')

        action_button = QAction(QIcon('bug.png'), '&Your button', self)
        action_button.setStatusTip('This is your button')
        action_button.setCheckable(True)
        action_button.triggered.connect(self.on_click)
        menu_file.addAction(action_button)

        menu_file.addSeparator()

        action_button_2 = QAction(QIcon('bug.png'), 'Your &button2', self)
        action_button_2.setStatusTip('This is your button2')
        action_button_2.setCheckable(True)
        action_button_2.triggered.connect(self.on_click)
        menu_file.addAction(action_button_2)

        # Main
        label_hello = QLabel('Hello!')
        label_hello.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label_hello)

    def on_click(self, s):
        print("click", s)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
