#!/usr/bin/env python
# coding: utf-8
import importlib.util
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class Example(QMainWindow):
    layout: QVBoxLayout = None
    module_name = 'Plugin'

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Plugin Test')

    def init_ui(self):
        base = QWidget()
        self.setCentralWidget(base)

        self.layout = QVBoxLayout()
        base.setLayout(self.layout)

        self.statusBar()

        open_file = QAction('Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Select plugin script.')
        open_file.triggered.connect(self.plugin_read_dialog)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file)

    def plugin_read_dialog(self):
        dialog = QFileDialog()
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            obj = self.add_module(file_path)
            self.layout.addWidget(obj)

    def add_module(self, file_path):
        # Reference:
        # https://docs.python.org/3/library/importlib.html
        spec = importlib.util.spec_from_file_location(self.module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # example: obj = module.Plugin()
        obj = eval('module.%s()' % self.module_name)
        return obj


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
