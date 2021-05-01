#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QMainWindow,
    QTextEdit,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('DockWidget')
        self.show()

    def initUI(self):
        main_te = QTextEdit()
        dock_left = QDockWidget("Left")
        dock_right = QDockWidget("Right")
        dock_top = QDockWidget("Top")
        dock_bottom = QDockWidget("Bottom")

        self.setCentralWidget(main_te)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_right)
        self.addDockWidget(Qt.TopDockWidgetArea, dock_top)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_bottom)
        self.statusBar()

        # Exit Action
        action_exit = self.make_action_exit()

        # Menu Bar
        mbar = self.menuBar()

        menu1 = mbar.addMenu('&File')
        menu1.addAction(action_exit)

        # Window Menu: toggle widget's visibility
        menu2 = mbar.addMenu('&Window')
        menu2.addAction(dock_left.toggleViewAction())
        menu2.addAction(dock_right.toggleViewAction())
        menu2.addAction(dock_top.toggleViewAction())
        menu2.addAction(dock_bottom.toggleViewAction())

        # Tool Bar
        tbar = self.addToolBar('Exit')
        tbar.addAction(action_exit)

    def make_action_exit(self):
        action_exit = QAction('&Exit', self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.setStatusTip('Quit Application')
        action_exit.triggered.connect(self.close)
        return action_exit


def main():
    app: QApplication = QApplication(sys.argv)
    ex: Example = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
