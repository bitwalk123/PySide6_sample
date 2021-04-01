#!/usr/bin/env python
# coding: utf-8

import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QCheckBox,
    QVBoxLayout,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("CheckBox")
        self.show()

    def initUI(self):
        cbox = QCheckBox('チェックボックス')
        cbox.toggle()
        cbox.stateChanged.connect(self.checkboxChanged)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(cbox)

    def checkboxChanged(self, state):
        sender = self.sender()
        if state == Qt.Checked:
            print('「' + sender.text() + '」にチェックを入れました。')
        else:
            print('「' + sender.text() + '」のチェックを外しました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
