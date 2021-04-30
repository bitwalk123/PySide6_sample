#!/usr/bin/env python
# coding: utf-8
# Reference:
# http://www2.hawaii.edu/~takebaya/cent110/gui/qtablewidget.html

import sys
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
)


class Example(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.resize(700, 400)
        self.setWindowTitle("My GUI Program")
        self.show()

    def initUI(self):
        self.initMenu()
        self.table = QTableWidget(1, 3)
        self.columnLabels = ["Make", "Model", "Price"]
        self.table.setHorizontalHeaderLabels(self.columnLabels)
        self.setCentralWidget(self.table)

    def initMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        open = QAction("Open", self)
        open.triggered.connect(self.openFile)
        fileMenu.addAction(open)
        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
        fileMenu.addAction(quit)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".")
        if (filename != ""):
            infile = open(filename, "r")
            lines = infile.readlines()
            infile.close()
            self.table.setRowCount(len(lines))
            for i in range(0, len(lines)):
                tokens = lines[i].strip().split(",")
                make = QTableWidgetItem(tokens[0])
                model = QTableWidgetItem(tokens[1])
                price = QTableWidgetItem(tokens[2])
                self.table.setItem(i,0,make)
                self.table.setItem(i,1,model)
                self.table.setItem(i,2,price)
            self.table.resizeColumnsToContents()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
