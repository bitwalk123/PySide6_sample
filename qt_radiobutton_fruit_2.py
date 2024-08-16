import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class ToggleButtonImage(QPushButton):
    def __init__(self, imgname: str, tooltip_str: str):
        super().__init__()
        self.setIcon(QIcon(imgname))
        self.setIconSize(QSize(32, 32))
        self.setToolTip(tooltip_str)
        self.setCheckable(True)
        self.setAutoExclusive(True)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('果物選択')

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        pb_apple = ToggleButtonImage('fruit_apple.png', '林檎')
        hbox.addWidget(pb_apple)
        pb_apple.toggle()

        pb_grape = ToggleButtonImage('fruit_grape.png', '葡萄')
        hbox.addWidget(pb_grape)

        pb_orange = ToggleButtonImage('fruit_orange.png', '蜜柑')
        pb_orange.setAutoExclusive(True)
        hbox.addWidget(pb_orange)

        self.but_group = but_group = QButtonGroup()
        but_group.addButton(pb_apple)
        but_group.addButton(pb_grape)
        but_group.addButton(pb_orange)
        but_group.buttonToggled.connect(self.selection_changed)

    def selection_changed(self, button, state):
        if state:
            status = 'オン'
        else:
            status = 'オフ'

        print('「%s」を%sにしました。' % (button.toolTip(), status))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
