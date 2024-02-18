#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication


class Example(QWebEngineView):
    def __init__(self, url: QUrl):
        super().__init__()
        self.loadFinished.connect(self.on_load_finished)
        self.resize(1000, 800)

        self.load(url)
        self.page().titleChanged.connect(self.setWindowTitle)

    def on_load_finished(self, flag: bool):
        if flag:
            self.page().toHtml(self.print_html)

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
