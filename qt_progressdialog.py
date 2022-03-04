#!/usr/bin/env python
# coding: utf-8

import sys
import time
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QProgressDialog,
    QPushButton,
)
from PySide6.QtCore import (
    QObject,
    QThread,
    Signal, Qt,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.setWindowTitle('ProgressDialog & Thread')
        self.resize(300, 100)

    def init_ui(self):
        but = QPushButton('START')
        but.clicked.connect(self.task_start)
        self.setCentralWidget(but)

    def task_start(self):
        button = self.sender()
        button.setEnabled(False)

        progress = QProgressDialog(labelText='Working...', parent=self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.setWindowTitle('status')
        progress.show()

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progressChanged.connect(progress.setValue)
        self.worker.progressCompleted.connect(lambda: self.task_end(button, progress))

        self.thread.start()

    def task_end(self, button, progress):
        button.setEnabled(True)
        progress.cancel()


class Worker(QObject):
    progressChanged = Signal(int)
    progressCompleted = Signal()
    finished = Signal()

    def run(self):
        for progress in range(0, 101):
            time.sleep(0.1)
            self.progressChanged.emit(progress)

        time.sleep(0.5)
        self.progressCompleted.emit()
        self.progressChanged.emit(0)
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
