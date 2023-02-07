#!/usr/bin/env python
# coding: utf-8
import importlib.util
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Example(QMainWindow):
    layout: QVBoxLayout = None
    class_name = 'Plugin'

    def __init__(self):
        super().__init__()
        self.counter_plugin = 0
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
            filename = dialog.selectedFiles()[0]
            print(filename)
            obj = self.add_module(filename)
            self.layout.addWidget(obj)

    def add_module(self, file_path: str) -> QPushButton:
        """Add module as plugin.

        Args:
            file_path: script path to load as plugin

        Returns:
            QPushButton: plugin widget to add main application

        Note:
            https://docs.python.org/3/library/importlib.html
        """
        module_name = 'plugin_%d' % self.counter_plugin
        self.counter_plugin += 1

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # example: obj = module.Plugin()
        obj = eval('module.%s()' % self.class_name)
        print(type(obj))
        return obj


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
