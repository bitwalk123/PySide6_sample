#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('CheckBox')

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        cbox_A = QCheckBox('チェックボックスＡ')
        cbox_A.toggle()
        cbox_A.stateChanged.connect(self.checkboxChanged)
        vbox.addWidget(cbox_A)

        cbox_B = QCheckBox('チェックボックスＢ')
        cbox_B.stateChanged.connect(self.checkboxChanged)
        vbox.addWidget(cbox_B)

        cbox_C = QCheckBox('チェックボックスＣ')
        cbox_C.stateChanged.connect(self.checkboxChanged)
        vbox.addWidget(cbox_C)

    def checkboxChanged(self, state):
        cbox = self.sender()
        if cbox.isChecked():
            print('「' + cbox.text() + '」にチェックを入れました。')
        else:
            print('「' + cbox.text() + '」のチェックを外しました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
