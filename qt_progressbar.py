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
    QThread,
    Signal,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.task_gen()

        self.setWindowTitle('ProgressBar & Thread')
        self.resize(300, 100)
        self.show()

    def initUI(self):
        self.but = QPushButton('START')
        self.but.clicked.connect(self.task_start)
        self.setCentralWidget(self.but)

        status_label = QLabel('Progress')
        status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.progbar = QProgressBar()
        self.progbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        status_bar = QStatusBar()
        status_bar.addWidget(status_label, 1)
        status_bar.addWidget(self.progbar, 2)

        self.setStatusBar(status_bar)

    def task_gen(self):
        self.task = TaskThread(self)
        self.task.progressChanged.connect(self.progbar.setValue)

    def task_start(self):
        self.but.setEnabled(False)
        self.task.start()
        self.task.progressCompleted.connect(self.task_end)

    def task_end(self):
        self.but.setEnabled(True)


class TaskThread(QThread):
    progressChanged = Signal(int)
    progressCompleted = Signal()

    def run(self):
        for progress in range(0, 101):
            time.sleep(0.1)
            self.progressChanged.emit(progress)

        self.progressCompleted.emit()
        self.exit(0)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
