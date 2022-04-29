#!/usr/bin/env python
# coding: utf-8

import sys
import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStatusBar,
)


class Example(QMainWindow):
    statusbar: QStatusBar = None
    msec = 3000

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QThread')
        # PySide6 version
        print('PySide', PySide6.__version__)

    def init_ui(self):
        # push button
        button = QPushButton('Download KNOPPIX')
        button.clicked.connect(self.on_click)
        button.setStatusTip('click to start downloading')
        self.setCentralWidget(button)
        # status bar
        self.statusbar = QStatusBar()
        self.statusbar.showMessage('Welcome!', self.msec)
        self.setStatusBar(self.statusbar)

    def on_click(self):
        self.statusbar.showMessage('start downloading')


class URLDownload(QObject):
    thread = None
    worker = None

    completed = Signal(bool)

    def __init__(self):
        super().__init__()

    def start(self):
        # threading
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # signal handling
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.downloadCompleted.connect(self.end)

        # start threading
        self.thread.start()

    def end(self, success: bool):
        self.completed.emit(success)


class Worker(QObject):
    downloadCompleted = Signal()
    finished = Signal()

    def __init__(self):
        super().__init__()

    def run(self):
        pass
        self.downloadCompleted.emit(success)
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    hello = Example()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
