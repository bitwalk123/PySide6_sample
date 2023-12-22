# https://doc.qt.io/qtforpython/examples/example_webenginewidgets__simplebrowser.html
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 WebEngineWidgets Example"""

import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStyle,
    QToolBar,
)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.address = None
        self.view = None

        url = 'https://www.qt.io/'
        self.init_ui(url)
        self.setWindowTitle('QWebEngineView example')
        self.resize(1000, 800)

    def init_ui(self, url_init: str):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        but_back = QPushButton()
        icon_back = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        but_back.setIcon(icon_back)
        but_back.clicked.connect(self.back)
        toolbar.addWidget(but_back)

        but_forward = QPushButton()
        icon_forward = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        but_forward.setIcon(icon_forward)
        but_forward.clicked.connect(self.forward)
        toolbar.addWidget(but_forward)

        self.address = address = QLineEdit()
        address.returnPressed.connect(self.load)
        toolbar.addWidget(address)

        self.view = view = QWebEngineView()
        self.setCentralWidget(view)

        address.setText(url_init)
        view.load(QUrl(url_init))
        view.page().titleChanged.connect(self.setWindowTitle)
        view.page().urlChanged.connect(self.url_changed)

    def load(self):
        url = QUrl.fromUserInput(self.address.text())
        if url.isValid():
            self.view.load(url)

    def back(self):
        self.view.page().triggerAction(QWebEnginePage.WebAction.Back)

    def forward(self):
        self.view.page().triggerAction(QWebEnginePage.WebAction.Forward)

    def url_changed(self, url):
        self.address.setText(url.toString())


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
