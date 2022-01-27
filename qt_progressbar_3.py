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
    QThread,
    Signal, Qt,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.setWindowTitle('ProgressBar & Thread (2)')
        self.resize(300, 100)

    def init_ui(self):
        but = QPushButton('START')
        but.clicked.connect(lambda: self.task_start(but))
        self.setCentralWidget(but)

    def task_start(self, button):
        progress = QProgressDialog(labelText='Working...', parent=self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.setRange(0, 0)
        progress.setWindowTitle('working')
        progress.show()

        button.setEnabled(False)

        task = TaskThread(self)
        task.start()
        task.progressCompleted.connect(lambda: self.task_end(button, progress))

    def task_end(self, button, progress):
        button.setEnabled(True)
        progress.cancel()


class TaskThread(QThread):
    progressCompleted = Signal()

    def run(self):
        for progress in range(0, 101):
            time.sleep(0.1)

        time.sleep(0.5)
        self.progressCompleted.emit()
        self.exit(0)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
