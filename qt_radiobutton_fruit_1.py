import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QRadioButton,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('果物選択')

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        rb_apple = QRadioButton('林檎')
        rb_apple.setIcon(QIcon('fruit_apple.png'))
        hbox.addWidget(rb_apple)
        rb_apple.toggle()

        rb_grape = QRadioButton('葡萄')
        rb_grape.setIcon(QIcon('fruit_grape.png'))
        hbox.addWidget(rb_grape)

        rb_orange = QRadioButton('蜜柑')
        rb_orange.setIcon(QIcon('fruit_orange.png'))
        hbox.addWidget(rb_orange)

        self.but_group = but_group = QButtonGroup()
        but_group.addButton(rb_apple)
        but_group.addButton(rb_grape)
        but_group.addButton(rb_orange)
        but_group.buttonToggled.connect(self.selection_changed)

    def selection_changed(self, button, state):
        if state:
            status = 'オン'
        else:
            status = 'オフ'

        print('「%s」を%sにしました。' % (button.text(), status))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
