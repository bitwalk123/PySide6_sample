#!/usr/bin/env python
# coding: utf-8

import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

DESCRIPTION = (
    "<p>"
    "表示したダイアログのウィンドウサイズを固定するには、"
    "showEvent() メソッドをオーバーライドして、ウィンドウサイズを固定する方法が簡単です。"
    "</p>"
    "<ul>"
    "<li>showEvent() は ウィンドウが実際に表示された直後に呼ばれます。</li>"
    "<li>レイアウト計算が終わった後なので、self.size() が確定しています。</li>"
    "</ul>"
)


class ExampleDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog')

        layout = QVBoxLayout()
        self.setLayout(layout)

        tedit = QTextEdit(DESCRIPTION)
        tedit.setStyleSheet("QTextEdit{background-color: white;}")
        tedit.setReadOnly(True)
        layout.addWidget(tedit)

        bbox = QDialogButtonBox()
        bbox.addButton(QDialogButtonBox.StandardButton.Ok)
        bbox.addButton(QDialogButtonBox.StandardButton.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)

    def showEvent(self, event):
        super().showEvent(event)
        # 表示後の最終サイズを固定
        self.setFixedSize(self.size())


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("メイン")

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton("ダイアログ表示")
        btn.clicked.connect(self.button_clicked)
        layout.addWidget(btn)

    @staticmethod
    def button_clicked():
        dlg = ExampleDlg()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            print("OK ボタンがクリックされました。")
        else:
            print("Cancel ボタンがクリックされました。")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
