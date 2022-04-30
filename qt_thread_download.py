#!/usr/bin/env python
# coding: utf-8
from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
)

from sample_download import download


class URLDownload(QObject):
    completed = Signal(bool)

    def __init__(self, url):
        super().__init__()
        self.thread = QThread()
        self.worker = URLDownloadWorker(url)

    def start(self):
        # move this instance to other thread
        self.worker.moveToThread(self.thread)
        # event handling
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.downloadCompleted.connect(self.end)
        # start the thread which starts self.worker.run
        self.thread.start()

    def end(self, success: bool):
        self.completed.emit(success)


class URLDownloadWorker(QObject):
    downloadCompleted = Signal(bool)
    finished = Signal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        status = download(self.url)
        self.downloadCompleted.emit(status)
        self.finished.emit()
