#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl, QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineDownloadRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QFileDialog


class Example(QWebEngineView):
    def __init__(self, url: QUrl):
        super().__init__()
        self.resize(1000, 800)

        self.load(url)
        self.page().titleChanged.connect(self.setWindowTitle)
        self.page().profile().downloadRequested.connect(
            self.on_downloadRequested
        )

    def createWindow(self, wwtype: QWebEnginePage.WebWindowType):
        action: QAction = self.pageAction(QWebEnginePage.WebAction.ViewSource)
        if action.isEnabled():
            self.page().toHtml(self.print_html)

    def on_downloadRequested(self, download: QWebEngineDownloadRequest):
        print(type(download))
        # Reference:
        # https://stackoverflow.com/questions/55963931/how-to-download-csv-file-with-qwebengineview-and-qurl
        old_path = download.url().path()  # download.path()
        suffix = QFileInfo(old_path).suffix()
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setDownloadDirectory(path)
            download.accept()

    @staticmethod
    def print_html(html: str):
        print(html)


def main(url: QUrl):
    app = QApplication()
    ex = Example(url)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url_init = QUrl('https://www.ueno-panda.jp/')
    main(url_init)
