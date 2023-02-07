#!/usr/bin/env python
# coding: utf-8
import importlib.util
import sys
from typing import Any

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def add_module(module_name: str, file_path: str, class_name: str) -> Any:
    """Add module

    Args:
        module_name (str): module name to add
        file_path (str): script path to load as plugin
        class_name (str): class name in the module to use

    Returns:
        Any: plugin instance to add into main application

    Note:
        https://docs.python.org/3/library/importlib.html
    """

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # example: obj = module.Plugin()
    obj = eval('module.%s()' % class_name)
    print(type(obj))
    return obj


class Example(QMainWindow):
    layout: QVBoxLayout = None
    class_name = 'Plugin'

    def __init__(self):
        super().__init__()
        self.id_plugin = 0
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
        """Dialog to read plugin script
        """
        dialog = QFileDialog()
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.add_plugin_widget(filename)

    def add_plugin_widget(self, filename: str):
        """Add plugin widget from specified filename

        Args:
            filename (str): plugin script to add
        """
        plugin_name = 'plugin_%d' % self.id_plugin
        self.id_plugin += 1

        obj = add_module(plugin_name, filename, self.class_name)
        self.layout.addWidget(obj)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
