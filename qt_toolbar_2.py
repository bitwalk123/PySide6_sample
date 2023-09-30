import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QStyle,
    QToolBar,
    QToolButton,
)


class Example(QMainWindow):
    list_file_recent = ['file 1', 'file 2', 'file 3']

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('ToolBar')

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add buttons to toolbar
        but_open = QToolButton()
        but_open.setText('Open')
        but_open.setToolTip('Open file')
        pixmap_open = QStyle.StandardPixmap.SP_DirOpenIcon
        icon_open = self.style().standardIcon(pixmap_open)
        but_open.setIcon(icon_open)
        but_open.clicked.connect(self.button_open_clicked)
        toolbar.addWidget(but_open)

        # Menu for open
        menu_open = QMenu(but_open)
        but_open.setMenu(menu_open)

        # Sub manu for recent files
        menu_recent = menu_open.addMenu('Recent files')
        for file_recent in self.list_file_recent:
            action_button = QAction(file_recent, self)
            action_button.triggered.connect(self.on_action_clicked)
            menu_recent.addAction(action_button)

    @staticmethod
    def button_open_clicked():
        dialog = QFileDialog()
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            print('selected :', filename)

    def on_action_clicked(self, event):
        action: QAction = self.sender()
        print('selected recent file :', action.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
