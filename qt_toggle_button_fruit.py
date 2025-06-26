import sys

from PySide6.QtCore import QSize, QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
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
        self.setWindowTitle('林檎と葡萄')

        grid = QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)

        self.apple = ToggleButtonImage('fruit_apple.png', '林檎')
        # 本来は toggled シグナルを使う
        self.apple.toggled.connect(self.button_toggled)
        grid.addWidget(self.apple, 0, 0)

        self.grape = ToggleButtonImage('fruit_grape.png', '葡萄')
        # clicked シグナルでもメソッドは呼び出されるが…
        self.grape.clicked.connect(self.button_toggled)
        grid.addWidget(self.grape, 0, 1)

        but_apple = QPushButton("toggle")
        but_apple.clicked.connect(self.toggle_apple)
        grid.addWidget(but_apple, 1, 0)

        but_grape = QPushButton("click")
        but_grape.clicked.connect(self.toggle_grape)
        grid.addWidget(but_grape, 1, 1)

    def button_toggled(self, state: bool):
        obj: QObject | ToggleButtonImage = self.sender()
        print(f"{obj.toolTip()} は {state} になりました。")

    def toggle_apple(self):
        """
        トグルボタンをマウスでクリックするのではなく、
        外部のコマンドで反転させても同じ効果が得られるかを確認する。

        toggled シグナルは　setChecked で適切に emit される
        したがって、button_toggled メソッドが呼び出される
        """
        if self.apple.isChecked():
            self.apple.setChecked(False)
        else:
            self.apple.setChecked(True)

    def toggle_grape(self):
        """
        トグルボタンをマウスでクリックするのではなく、
        外部のコマンドで反転させても同じ効果が得られるかを確認する。

        clicked シグナルは　setChecked では emit されない
        したがって、button_toggled メソッドが呼び出されることはない      """
        if self.grape.isChecked():
            self.grape.setChecked(False)
        else:
            self.grape.setChecked(True)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
