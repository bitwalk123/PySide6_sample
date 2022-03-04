#!/usr/bin/env python
# coding: utf-8

import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
)
from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
)


class Example(QMainWindow):
    thread = None
    worker = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.setWindowTitle('ProgressBar & Thread (2)')
        self.resize(300, 100)

    def init_ui(self):
        but = QPushButton('START')
        but.clicked.connect(lambda: self.task_start(but, progbar))
        self.setCentralWidget(but)

        status_label = QLabel('Progress')
        status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        progbar = QProgressBar()
        progbar.setRange(0, 1)
        progbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        status_bar = QStatusBar()
        status_bar.addWidget(status_label, 1)
        status_bar.addWidget(progbar, 2)

        self.setStatusBar(status_bar)

    def task_start(self, button, progbar):
        button.setEnabled(False)
        progbar.setRange(0, 0)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressCompleted.connect(lambda: self.task_end(button, progbar))

        self.thread.start()

    def task_end(self, button, progbar):
        button.setEnabled(True)
        progbar.setRange(0, 1)


class Worker(QObject):
    progressCompleted = Signal()
    finished = Signal()

    def run(self):
        for progress in range(0, 101):
            time.sleep(0.1)

        time.sleep(0.5)
        self.progressCompleted.emit()
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
