#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QFileInfo, QUrl
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QFileDialog


class Example(QWebEngineView):
    def __init__(self, url: QUrl):
        super().__init__()
        self.status_load = False
        self.loadFinished.connect(self.on_load_finished)
        self.resize(1000, 800)

        self.load(url)
        self.page().titleChanged.connect(self.setWindowTitle)
        self.page().profile().downloadRequested.connect(
            self.on_download_requested
        )

    def createWindow(self, wwtype: QWebEnginePage.WebWindowType):
        action: QAction = self.pageAction(QWebEnginePage.WebAction.ViewSource)
        if action.isEnabled():
            self.page().toHtml(self.print_html)

    def on_download_requested(self, download: QWebEngineDownloadRequest):
        # Reference:
        # https://stackoverflow.com/questions/55963931/how-to-download-csv-file-with-qwebengineview-and-qurl
        url_path = download.url().path()  # download.path()
        if url_path == '/':
            url_path = 'index.html'
        suffix = QFileInfo(url_path).suffix()
        path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', url_path, '*.' + suffix
        )
        if path:
            download.setDownloadDirectory(path)
            download.accept()

    def on_load_finished(self, flag: bool):
        self.status_load = flag
        page: QWebEnginePage = self.page()
        #jscript = 'document.documentElement.outerHTML'
        jscript = """
        var element = document.getElementById('banner');
        element.innerHTML;
        """
        page.runJavaScript(
            jscript,
            0, self.print_html
        )


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
