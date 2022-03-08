#!/usr/bin/env python
# coding: utf-8
# reference
# https://github.com/andriyantohalim/PySide2_Tutorial
import sys
import time

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPlainTextEdit,
)


def timeit(f: callable):
    """
    Reference:
    https://stackoverflow.com/questions/5478351/python-time-measure-function
    """

    def wrap(*args, **kwargs):
        time_start = time.time()
        ret = f(*args, **kwargs)
        time_end = time.time()
        msec_elapsed = (time_end - time_start) * 1000.0
        print('{:s} function took {:.3f} ms'.format(f.__name__, msec_elapsed))

        return ret

    return wrap


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
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            data = self.read_data(filename)
            self.editor.setPlainText(data)

    @timeit
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
