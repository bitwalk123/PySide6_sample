#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("RadioButton")
        self.show()

    def initUI(self):
        rb_A = QRadioButton('ラジオボタンＡ')
        # rad_A.toggle()
        rb_A.toggled.connect(self.checkboxChanged)

        rb_B = QRadioButton('ラジオボタンＢ')
        rb_B.toggled.connect(self.checkboxChanged)

        rb_C = QRadioButton('ラジオボタンＣ')
        rb_C.toggled.connect(self.checkboxChanged)

        # Reference:
        # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QRadioButton.html
        #
        # Radio buttons are autoExclusive by default. If auto-exclusive is
        # enabled, radio buttons that belong to the same parent widget behave
        # as if they were part of the same exclusive button group. If you need
        # multiple exclusive button groups for radio buttons that belong to the
        # same parent widget, put them into a QButtonGroup .
        rb_group = QButtonGroup()
        rb_group.addButton(rb_A)
        rb_group.addButton(rb_B)
        rb_group.addButton(rb_C)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(rb_A)
        vbox.addWidget(rb_B)
        vbox.addWidget(rb_C)

    def checkboxChanged(self, state):
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            print('「' + rb.text() + '」にチェックを入れました。')
        else:
            print('「' + rb.text() + '」のチェックを外しました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
