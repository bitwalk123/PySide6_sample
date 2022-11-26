# Reference:
# https://doc.qt.io/qtforpython/examples/example_webenginewidgets__simplebrowser.html
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 WebEngineWidgets Example"""

import sys
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QToolBar,
)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PySide6 WebEngineWidgets Example')

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/left-32.png'))
        self.backButton.clicked.connect(self.back)
        self.toolBar.addWidget(self.backButton)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/right-32.png'))
        self.forwardButton.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forwardButton)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.addressLineEdit)

        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)

        initialUrl = 'http://qt.io'
        self.addressLineEdit.setText(initialUrl)
        self.webEngineView.load(QUrl(initialUrl))
        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)

    @Slot()
    def load(self):
        url = QUrl.fromUserInput(self.addressLineEdit.text())
        if url.isValid():
            self.webEngineView.load(url)

    @Slot()
    def back(self):
        # self.webEngineView.page().triggerAction(QWebEnginePage.Back)
        self.webEngineView.page().triggerAction(QWebEnginePage.WebAction.Back)

    @Slot()
    def forward(self):
        # self.webEngineView.page().triggerAction(QWebEnginePage.Forward)
        self.webEngineView.page().triggerAction(QWebEnginePage.WebAction.Forward)

    @Slot(QUrl)
    def urlChanged(self, url):
        self.addressLineEdit.setText(url.toString())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    availableGeometry = ex.screen().availableGeometry()
    ex.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2 / 3)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
