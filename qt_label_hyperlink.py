#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Label (Hyper Link)')

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        url = 'https://doc.qt.io/qtforpython-6/'
        msg = 'Qt for Python'
        lab = QLabel()
        lab.setText('<a href="%s">%s</a>' % (url, msg))
        lab.setOpenExternalLinks(True)
        lab.setContentsMargins(10, 0, 10, 0)
        """
        lab.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        """
        vbox.addWidget(lab)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
