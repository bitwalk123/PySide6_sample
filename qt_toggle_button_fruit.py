import sys

from PySide6.QtCore import QSize, QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ToggleButtonImage(QPushButton):
    def __init__(self, imgname: str, tooltip_str: str):
        super().__init__()
        self.setIcon(QIcon(imgname))
        self.setIconSize(QSize(64, 64))
        self.setToolTip(tooltip_str)
        self.setCheckable(True)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('林檎')

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        self.setLayout(vbox)

        self.apple = ToggleButtonImage('fruit_apple.png', '林檎')
        self.apple.toggled.connect(self.button_toggled)
        vbox.addWidget(self.apple)

        but_apple = QPushButton("トグル")
        but_apple.clicked.connect(self.toggle_apple)
        vbox.addWidget(but_apple)

    def button_toggled(self, state: bool):
        print(f"{state} になりました。")

    def toggle_apple(self):
        """
        トグルボタンをマウスでクリックするのではなく、
        外部のコマンドで反転させても同じ効果が得られるかを確認する。
        """
        if self.apple.isChecked():
            self.apple.setChecked(False)
        else:
            self.apple.setChecked(True)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
