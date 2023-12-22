# https://doc.qt.io/qtforpython/examples/example_webenginewidgets__simplebrowser.html
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 WebEngineWidgets Example"""

import sys

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStyle,
    QToolBar,
)


class WebToolBar(QToolBar):
    Back = Signal()
    Forward = Signal()
    Load = Signal(str)

    def __init__(self):
        super().__init__()
        self.address = None
        self.init_ui()

    def init_ui(self):
        but_back = QPushButton()
        icon_back = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        but_back.setIcon(icon_back)
        but_back.clicked.connect(self.back)
        self.addWidget(but_back)

        but_forward = QPushButton()
        icon_forward = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        but_forward.setIcon(icon_forward)
        but_forward.clicked.connect(self.forward)
        self.addWidget(but_forward)

        self.address = address = QLineEdit()
        address.returnPressed.connect(self.load)
        self.addWidget(address)

    def back(self):
        self.Back.emit()

    def forward(self):
        self.Forward.emit()

    def load(self):
        lineedit: QLineEdit = self.sender()
        self.Load.emit(lineedit.text())

    def setURL(self, url: QUrl):
        self.address.setText(url.toString())


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toolbar = None
        self.view = None

        url = QUrl('https://www.qt.io/')
        self.init_ui(url)
        self.resize(1000, 800)

    def init_ui(self, url_init: QUrl):
        self.toolbar = toolbar = WebToolBar()
        toolbar.Back.connect(self.back)
        toolbar.Forward.connect(self.forward)
        toolbar.Load.connect(self.load)
        self.addToolBar(toolbar)

        self.view = view = QWebEngineView()
        self.setCentralWidget(view)

        toolbar.setURL(url_init)
        view.load(url_init)
        view.page().titleChanged.connect(self.setWindowTitle)
        view.page().urlChanged.connect(self.url_changed)

    def load(self, url_str: str):
        url = QUrl.fromUserInput(url_str)
        if url.isValid():
            self.view.load(url)

    def back(self):
        self.view.page().triggerAction(QWebEnginePage.WebAction.Back)

    def forward(self):
        self.view.page().triggerAction(QWebEnginePage.WebAction.Forward)

    def url_changed(self, url: QUrl):
        self.toolbar.setURL(url)


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
