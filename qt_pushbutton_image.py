import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


def get_colored_icon(image: str, color: str):
    """
    get_colored_icon
    :param image: file name of image
    :param color: color code
    :return: QIcon filled with specified color
    """
    pixmap = QPixmap(image)
    mask = pixmap.createMaskFromColor(QColor('transparent'), Qt.MaskInColor)
    pixmap.fill(QColor(color))
    pixmap.setMask(mask)

    return QIcon(pixmap)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('PushButton')

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        image = 'circle.png'
        for color in ['red', 'green', 'blue']:
            icon = get_colored_icon(image, color)
            btn = QPushButton(icon, color)
            btn.setStyleSheet('text-align:left; font-size:18pt;')
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(self.button_clicked)
            layout.addWidget(btn)

    def button_clicked(self):
        obj = self.sender()
        print('\'%s\' button is clicked.' % obj.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
