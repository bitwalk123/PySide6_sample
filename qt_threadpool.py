#!/usr/bin/env python
# coding: utf-8

import sys
import time

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QApplication,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class WorkerSignal(QObject):
    progress = Signal(str)
    finished = Signal()


class Worker(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignal()

    @Slot()
    def run(self):
        for count in range(0, 5):
            time.sleep(1)
            self.signals.progress.emit('%d%% done.' % (count * 100 / 4))
        self.signals.finished.emit()


class Example(QWidget):
    log: QPlainTextEdit = None

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.init_ui()
        self.show_log(
            'Multithreading with maximum %d threads' % self.threadpool.maxThreadCount()
        )
        self.setWindowTitle('QThreadPool')
        self.resize(400, 200)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton('START')
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

        self.log = QPlainTextEdit()
        self.log.setMaximumBlockCount(1000)
        self.log.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.log)

    def button_clicked(self):
        obj = self.sender()
        self.show_log('%s button is clicked and starts thread task.' % obj.text())

        worker = Worker()
        worker.signals.progress.connect(self.show_log)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def thread_complete(self):
        self.show_log('Thread completed!')

    def show_log(self, msg: str):
        self.log.insertPlainText(msg + '\n')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
