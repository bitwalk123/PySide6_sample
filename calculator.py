#!/usr/bin/env python
# coding: utf-8

import math
import queue
import re
import sys
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLayout,
    QLCDNumber,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Calculator(QWidget):
    # Key Layout
    keys_info = [
        {"label": "Ｃ", "x": 0, "y": 1, "w": 1, "h": 1, "name": "Cls", "method": "on_clear"},
        {"label": "√", "x": 1, "y": 1, "w": 1, "h": 1, "name": "Fnc", "method": "on_function"},
        {"label": "±", "x": 2, "y": 1, "w": 1, "h": 1, "name": "Fnc", "method": "on_function"},
        {"label": "÷", "x": 3, "y": 1, "w": 1, "h": 1, "name": "Ope", "method": "on_operation"},
        {"label": "７", "x": 0, "y": 2, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "８", "x": 1, "y": 2, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "９", "x": 2, "y": 2, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "×", "x": 3, "y": 2, "w": 1, "h": 1, "name": "Ope", "method": "on_operation"},
        {"label": "４", "x": 0, "y": 3, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "５", "x": 1, "y": 3, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "６", "x": 2, "y": 3, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "−", "x": 3, "y": 3, "w": 1, "h": 1, "name": "Ope", "method": "on_operation"},
        {"label": "１", "x": 0, "y": 4, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "２", "x": 1, "y": 4, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "３", "x": 2, "y": 4, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "＋", "x": 3, "y": 4, "w": 1, "h": 2, "name": "Ope", "method": "on_operation"},
        {"label": "０", "x": 0, "y": 5, "w": 1, "h": 1, "name": "Key", "method": "on_number"},
        {"label": "・", "x": 1, "y": 5, "w": 1, "h": 1, "name": "Key", "method": "on_dot"},
        {"label": "＝", "x": 2, "y": 5, "w": 1, "h": 1, "name": "Ope", "method": "on_equal"},
    ]

    # max length
    max_chars = 12

    # operation flag
    flag_dot = False
    flag_operation = False
    flag_error = False

    # register for calculation
    reg = queue.Queue()

    # regular expression
    re1 = re.compile("([\-0-9]+)\.$")
    re2 = re.compile("([\-0-9]+\.)0$")

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Calculator')
        self.setWindowIcon(QIcon(self.get_app_pixmap()))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def init_ui(self):
        grid = QGridLayout()
        grid.setHorizontalSpacing(2)
        grid.setVerticalSpacing(2)
        # Reference
        # https://stackoverflow.com/questions/16673074/how-can-i-fully-disable-resizing-a-window-including-the-resize-icon-when-the-mou
        grid.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(grid)

        # This is register
        self.ent = Register()

        # This is display value of register
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(self.max_chars + 2)
        self.lcd.setSmallDecimalPoint(True)
        self.lcd.display(self.ent.get_text())
        self.lcd.setStyleSheet("QLCDNumber {background-color:darkgreen; color:yellow;}")
        self.lcd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(self.lcd, 0, 0, 1, 4)
        grid.setRowMinimumHeight(0, 40)

        for key in self.keys_info:
            but = QPushButton(key['label'])
            method_name = key['method']
            method = getattr(self, method_name)
            but.clicked.connect(method)
            but.setStyleSheet("QPushButton {font-size:12pt; padding:5px 30px; color:darkgreen;}")
            but.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid.addWidget(but, key['y'], key['x'], key['h'], key['w'])

    def get_app_pixmap(self):
        base64data = b'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'
        byte_array = QByteArray.fromBase64(base64data)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)

        return pixmap

    # -------------------------------------------------------------------------
    #  get_display_string
    #
    #  argument
    #    value : value to display
    #
    #  return
    #    string to display
    # -------------------------------------------------------------------------
    def get_display_string(self, value):
        if self.flag_error:
            return value

        str_value = str(value)
        self.ent.set_text(str_value)

        m = pow(10.0, self.max_chars)
        value_int = int(value)
        if abs(value_int) > 0:
            value_int_length = int(math.log10(abs(value_int))) + 1
            if value_int_length < self.max_chars:
                if abs(value - value_int) < 1 / m:
                    str_value = str(value_int)
                else:
                    str_value = str(int(value * m) / m)
                    while len(str_value) > self.max_chars:
                        m = m / 10
                        str_value = str(int(value * m) / m)
            else:
                str_value = '{:.3e}'.format(value)
        else:
            if value < 1 / m:
                str_value = '{:.3e}'.format(value)
            else:
                str_value = str(int(value * m) / m)

        result = self.re2.match(str_value)
        if result:
            str_value = result.group(1)
            return str_value

        return str_value

    # -------------------------------------------------------------------------
    #  get_function_result
    #
    #  arguments
    #    text  : function operator
    #    value : value of function parameter
    #
    #  return
    #    value calculated specified function
    # -------------------------------------------------------------------------
    def get_function_result(self, text, value):
        # sign
        if text == "±":
            return value * -1
        # square root
        if text == "√":
            try:
                return math.sqrt(value)
            except Exception as e:
                self.flag_error = True
                # return e
                return "Error"

    # -------------------------------------------------------------------------
    #  get_operator
    #
    #  argument
    #    text : label string of calculator key pad
    #
    #  return
    #    operator string
    # -------------------------------------------------------------------------
    def get_operator(self, text):
        if text == "＋":
            return "+"
        if text == "−":
            return "-"
        if text == "×":
            return "*"
        if text == "÷":
            return "/"

    # -------------------------------------------------------------------------
    #  set_display
    #
    #  argument
    #    text : string to display
    # -------------------------------------------------------------------------
    def set_display(self, text):
        self.lcd.display(text)

    # -------------------------------------------------------------------------
    #  zenkaku_to_hankaku
    #
    #  argument
    #    text : zenkaku string
    #
    #  return
    #    hankaku (ascii) string
    # -------------------------------------------------------------------------
    def zenkaku_to_hankaku(self, text):
        # ref: https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf
        return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

    # =========================================================================
    #  BINDINGS
    # =========================================================================
    # -------------------------------------------------------------------------
    #  on_clear
    # -------------------------------------------------------------------------
    def on_clear(self):
        # display
        self.ent.init()
        self.set_display(self.ent.get_text())

        # clear flag
        self.flag_dot = False
        self.flag_operation = False
        self.flag_error = False

    # -------------------------------------------------------------------------
    #  on_dot
    # -------------------------------------------------------------------------
    def on_dot(self):
        if self.flag_error:
            return

        # flag
        self.flag_dot = True

    # -------------------------------------------------------------------------
    #  on_equal
    # -------------------------------------------------------------------------
    def on_equal(self):
        if self.flag_error:
            return

        expr = ""
        while not self.reg.empty():
            expr += self.reg.get()

        expr += self.ent.get_text()

        try:
            result = eval(expr)
        except Exception as e:
            self.flag_error = True
            # result = e
            result = "Error"

        disp_new = self.get_display_string(result)

        # display
        self.set_display(disp_new)

        # flag
        self.flag_operation = True

    # -------------------------------------------------------------------------
    #  on_function
    # -------------------------------------------------------------------------
    def on_function(self):
        button = self.sender()
        if self.flag_error:
            return

        # get current value displayed
        value_current = float(self.ent.get_text())

        # get string from key label
        text = button.text()

        value_new = self.get_function_result(text, value_current)
        disp_new = self.get_display_string(value_new)

        # display
        self.set_display(disp_new)

        # flag
        self.flag_operation = True

    # -------------------------------------------------------------------------
    #  on_operation
    # -------------------------------------------------------------------------
    def on_operation(self):
        button = self.sender()
        if self.flag_error:
            return

        # get current string displayed
        disp_current = self.ent.get_text()
        self.reg.put(disp_current)

        # get string from key label
        text = button.text()
        self.reg.put(self.get_operator(text))

        # flag
        self.flag_operation = True
        self.flag_dot = False

    # -------------------------------------------------------------------------
    #  on_number
    # -------------------------------------------------------------------------
    def on_number(self):
        button = self.sender()
        if self.flag_error:
            return

        # get current string displayed
        disp_current = self.ent.get_text()

        # get string from key label
        text = button.text()
        text_ascii = self.zenkaku_to_hankaku(text)

        # update string to display
        if self.flag_operation:
            disp_new = text_ascii + "."
            self.flag_operation = False
        else:
            if disp_current == "0.":
                if self.flag_dot:
                    disp_new = disp_current + text_ascii
                else:
                    disp_new = text_ascii + "."
            else:
                # check charcter length (digit)
                if len(disp_current) > self.max_chars:
                    return

                if self.flag_dot:
                    disp_new = disp_current + text_ascii
                else:
                    result = self.re1.match(disp_current)
                    if result:
                        disp_new = result.group(1) + text_ascii + "."
                    else:
                        disp_new = disp_current + text_ascii

        self.ent.set_text(disp_new)
        self.set_display(disp_new)


class Register():
    text = None

    def __init__(self):
        self.init()

    def init(self):
        self.text = '0.'

    def get_text(self):
        return (self.text)

    def set_text(self, str):
        self.text = str


def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
