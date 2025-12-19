#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPlainTextEdit,
)




class Example(QMainWindow):
    editor = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')

    def init_ui(self):
        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)
        self.statusBar()

        open_file = QAction('Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new file.')
        open_file.triggered.connect(self.show_dialog)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file)

    def show_dialog(self):
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            data = self.read_data(filename)
            self.editor.setPlainText(data)
        else:
            print("Canceled!")

    def read_data(self, filename):
        f = open(filename, 'r', encoding='UTF-8')
        data = f.read()
        return data


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
