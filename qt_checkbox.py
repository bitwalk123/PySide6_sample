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
        cbox_A = QCheckBox('チェックボックスＡ')
        cbox_A.toggle()
        cbox_A.stateChanged.connect(self.checkboxChanged)

        cbox_B = QCheckBox('チェックボックスＢ')
        cbox_B.stateChanged.connect(self.checkboxChanged)

        cbox_C = QCheckBox('チェックボックスＣ')
        cbox_C.stateChanged.connect(self.checkboxChanged)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(cbox_A)
        vbox.addWidget(cbox_B)
        vbox.addWidget(cbox_C)

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
