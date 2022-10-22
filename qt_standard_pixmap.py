# Reference:
# https://www.pythonguis.com/faq/built-in-qicons-pyqt/
import sys

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QStyle,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Qt Standard Pixmap')

    def init_ui(self):
        icons = sorted([attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")])
        print(icons)
        layout = QGridLayout()
        for n, name in enumerate(icons):
            btn = QPushButton(name)
            btn.setStyleSheet('text-align:left;')

            pixmap_icon = getattr(QStyle, name)
            icon = self.style().standardIcon(pixmap_icon)
            btn.setIcon(icon)
            layout.addWidget(btn, n / 4, n % 4)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
