#!/usr/bin/env python
# coding: utf-8
import os
import sys
import time

import pandas as pd
from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
)
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QProgressDialog,
)


def timeit(f: callable):
    def wrap(*args, **kwargs):
        time_start = time.time()
        ret = f(*args, **kwargs)
        time_end = time.time()
        msec_elapsed = (time_end - time_start) * 1000.0
        print('{:s} function took {:.3f} ms'.format(f.__name__, msec_elapsed))

        return ret

    return wrap


class CSVReader(QObject):
    readCompleted = Signal(pd.DataFrame)
    finished = Signal()

    def __init__(self, csvfile):
        super().__init__()
        self.csvfile = csvfile

    @timeit
    def run(self):
        df = pd.read_csv(self.csvfile)
        self.readCompleted.emit(df)
        self.finished.emit()


class WorkInProgress(QProgressDialog):
    def __init__(self, parent):
        super().__init__(labelText='Working...', parent=parent)
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.setRange(0, 0)
        self.setWindowTitle('progress')


class Example(QMainWindow):
    thread = None
    reader = None

    def __init__(self):
        super().__init__()
        self.progress = WorkInProgress(self)
        self.init_ui()
        self.setWindowTitle('FileDialog')

    def init_ui(self):
        self.statusBar()

        open_file = QAction('Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open new file.')
        open_file.triggered.connect(self.show_dialog)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file)

    def show_dialog(self):
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV file',
            filter='CSV File (*.csv)'
        )
        csvfile = selection[0]
        self.read_csv(csvfile)

    def read_csv(self, csvfile):
        if not os.path.exists(csvfile):
            return pd.DataFrame()

        # threading
        self.reader = CSVReader(csvfile)
        self.thread = QThread()
        self.reader.moveToThread(self.thread)
        # controller
        self.thread.started.connect(self.reader.run)
        self.reader.finished.connect(self.thread.quit)
        self.reader.finished.connect(self.reader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.reader.readCompleted.connect(self.handle_results)
        # start threading
        self.thread.start()
        self.progress.show()

    def handle_results(self, df):
        self.progress.cancel()
        print(df.shape)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
