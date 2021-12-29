#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import QDir
from PySide6.QtWidgets import (
    QApplication,
    QFileSystemModel,
    QMainWindow,
    QTreeView,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('TreeView')

    def init_ui(self):
        tree = QTreeView()
        self.setCentralWidget(tree)

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        tree.setModel(model)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
