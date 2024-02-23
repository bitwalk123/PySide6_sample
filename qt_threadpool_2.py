#!/usr/bin/env python
# coding: utf-8

import sys
import time

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStatusBar,
)


class WorkerSignal(QObject):
    threadFinished = Signal()
    threadProgress = Signal(int)


class Worker(QRunnable, WorkerSignal):
    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.threadProgress.emit(i + 1)
        self.threadFinished.emit()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QThreadPool')
        self.threadpool = QThreadPool()

        self.btn = QPushButton('START')
        self.btn.setStyleSheet("""
            QPushButton:disabled {color: gray; background-color: lightgray;}
        """)
        self.btn.clicked.connect(self.button_clicked)
        self.setCentralWidget(self.btn)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        statusbar.addPermanentWidget(self.pbar, stretch=1)

    def button_clicked(self):
        self.btn.setEnabled(False)
        worker = Worker()
        worker.threadProgress.connect(self.on_status_update)
        worker.threadFinished.connect(self.on_completed)
        self.threadpool.start(worker)

    def on_completed(self):
        self.btn.setEnabled(True)
        self.pbar.reset()

    def on_status_update(self, progress: int):
        self.pbar.setValue(progress)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
