#!/usr/bin/env python
# coding: utf-8
import sys

import PySide6
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStatusBar,
)

from qt_thread_download import URLDownload
from qt_thread_progress import EndlessProgressDialog


class Example(QMainWindow):
    statusbar: QStatusBar = None
    msec = 3000
    obj = None
    # sample file to download
    url = 'https://ftp.kddilabs.jp/Linux/distributions/PLD/iso/2.0/i386/pld-2.0-MINI.i386.iso'

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QThread')
        # PySide6 version
        print('PySide', PySide6.__version__)

    def init_ui(self):
        # push button
        button = QPushButton('Download large file')
        button.clicked.connect(self.on_click)
        button.setStatusTip('click to start downloading')
        self.setCentralWidget(button)
        # status bar
        self.statusbar = QStatusBar()
        self.statusbar.showMessage('Welcome!', self.msec)
        self.setStatusBar(self.statusbar)

    def on_click(self):
        # show progress dialog
        self.dlg = EndlessProgressDialog(self)
        self.dlg.show()
        # update status
        self.statusbar.showMessage('downloading, ...')
        # instance for download in thread
        self.obj = URLDownload(self.url)
        self.obj.completed.connect(self.download_finish)
        self.obj.start()

    def download_finish(self, success: bool):
        print(success)
        # stop and delete dialog
        self.dlg.cancel()
        # update status
        self.statusbar.showMessage('finish downloading', self.msec)


def main():
    app = QApplication(sys.argv)
    hello = Example()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
