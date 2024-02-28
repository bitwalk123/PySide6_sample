#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFontDatabase
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication


class Example(QWebEngineView):
    def __init__(self, url: QUrl):
        super().__init__()
        self.load(url)
        page: QWebEnginePage = self.page()
        page.titleChanged.connect(self.setWindowTitle)

        settings = page.settings()
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, 'Noto Sans CJK JP')
        settings.setFontFamily(QWebEngineSettings.FontFamily.SansSerifFont, 'Noto Sans CJK JP')
        settings.setFontFamily(QWebEngineSettings.FontFamily.SerifFont, 'Noto Serif CJK JP')
        settings.setFontFamily(QWebEngineSettings.FontFamily.FixedFont, 'Noto Sans Mono CJK JP')
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)

        self.resize(1000, 800)


def main(url: QUrl):
    app = QApplication()
    ex = Example(url)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url_init = QUrl('https://www.ueno-panda.jp/')
    main(url_init)
