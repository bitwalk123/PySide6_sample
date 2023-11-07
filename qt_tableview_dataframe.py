#!/usr/bin/env python
# coding: utf-8
# Reference
# https://doc.qt.io/qtforpython/examples/example_external__pandas.html
import pandas as pd
import sys
from PySide6.QtWidgets import (
    QTableView,
    QApplication,
    QMainWindow,
)

from qt_model_dataframe import PandasModel


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        df = pd.read_csv('iris.csv')
        self.init_ui(df)
        self.setWindowTitle('QTableView')
        self.resize(800, 600)

    def init_ui(self, df: pd.DataFrame):
        view = QTableView()
        self.setCentralWidget(view)

        # view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        # view.setSelectionBehavior(QTableView.SelectRows)

        model = PandasModel(df)
        view.setModel(model)


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
