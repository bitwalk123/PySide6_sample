import sys
from PySide6.QtCore import (
    QSize,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
    QPaintDevice,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)


class Example(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.initUI()
        self.setWindowTitle('QScrollArea')

    def initUI(self):
        # base widget to display on the QScrollArea
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)

        # Grid Layout
        grid = QGridLayout()
        base.setLayout(grid)

        # Font Size
        font_size: int = 24
        # Font Pixel
        font_pixel: int = int(font_size * QPaintDevice.physicalDpiY(self) / 72)
        # Font object
        font = QFont()
        font.setPointSize(font_size)

        # QLineEdit (Entry)
        ledit = QLineEdit()
        ledit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ledit.setFont(font)
        grid.addWidget(ledit, 0, 0)

        # QPushButton
        button = QPushButton()
        button.setIcon(QIcon('pencil.png'))
        button.setIconSize(QSize(font_pixel, font_pixel))
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        grid.addWidget(button, 0, 1)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
