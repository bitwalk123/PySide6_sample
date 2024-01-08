#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication


class Example(QWebEngineView):
    def __init__(self, url: QUrl):
        super().__init__()
        self.load(url)
        self.loadFinished.connect(self.on_load_finished)
        page: QWebEnginePage = self.page()
        page.titleChanged.connect(self.setWindowTitle)
        self.resize(1000, 800)

    def on_load_finished(self, flag: bool) -> bool:
        if not flag:
            return False
        page: QWebEnginePage = self.page()
        page.runJavaScript(
            "document.documentElement.outerHTML",
            0, self.print_html
        )
        return True

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
