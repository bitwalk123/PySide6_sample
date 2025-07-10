import sys

from PySide6.QtCore import QMargins
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class LabelSmall(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("""
            QLabel {
                margin: 0 5;
            }
        """)
        font = QFont()
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(6)
        self.setFont(font)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QLabel')

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(vbox)

        lab = LabelSmall('ラベルは文字を表示します。')

        vbox.addWidget(lab)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
