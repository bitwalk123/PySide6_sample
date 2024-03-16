import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QSpinBox')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        sb = QSpinBox()
        sb.setRange(0, 100)
        sb.setAlignment(Qt.AlignmentFlag.AlignRight)
        sb.valueChanged.connect(self.show_value)
        vbox.addWidget(sb)

    def show_value(self, value: int):
        print('%d になりました。' % value)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
