#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QDial,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    value_old = 0
    value_min = 0
    value_max = 100
    value_delta = 10

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dial')
        self.initUI()
        self.resize(200, 200)

    def initUI(self):
        dial = QDial()
        dial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        dial.setNotchesVisible(True)
        dial.setMinimum(self.value_min)
        dial.setMaximum(self.value_max)
        dial.setValue(self.value_old)
        dial.valueChanged.connect(lambda: self.dialer_changed(dial, label))

        label = QLabel()
        self.disp_value(label, self.value_old)

        vbox = QVBoxLayout()
        vbox.addWidget(dial)
        vbox.addWidget(label)
        self.setLayout(vbox)
        self.show()

    def dialer_changed(self, d: QDial, lab: QLabel):
        value = d.value()

        if (abs(value - self.value_old) > self.value_delta):
            d.setValue(self.value_old)
            value = self.value_old
        else:
            self.value_old = value

        self.disp_value(lab, value)

    def disp_value(self, lab: QLabel, x: int):
        lab.setText('value : ' + str(x))


def main():
    app = QApplication(sys.argv)
    # print(QStyleFactory.keys())
    app.setStyle('Fusion')
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
