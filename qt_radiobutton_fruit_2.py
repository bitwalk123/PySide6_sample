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


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('果物選択')

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        size = QSize(32, 32)

        pb_apple = QPushButton()
        pb_apple.setIcon(QIcon('fruit_apple.png'))
        pb_apple.setIconSize(size)
        pb_apple.setToolTip('林檎')
        pb_apple.setCheckable(True)
        pb_apple.setAutoExclusive(True)
        hbox.addWidget(pb_apple)
        pb_apple.toggle()

        pb_grape = QPushButton()
        pb_grape.setIcon(QIcon('fruit_grape.png'))
        pb_grape.setIconSize(size)
        pb_grape.setToolTip('葡萄')
        pb_grape.setCheckable(True)
        pb_grape.setAutoExclusive(True)
        hbox.addWidget(pb_grape)

        pb_orange = QPushButton()
        pb_orange.setIcon(QIcon('fruit_orange.png'))
        pb_orange.setIconSize(size)
        pb_orange.setToolTip('蜜柑')
        pb_orange.setCheckable(True)
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
