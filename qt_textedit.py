import sys
from PySide6.QtWidgets import (
    QApplication,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTextEdit")

        layout = QVBoxLayout()
        self.setLayout(layout)

        tedit = QTextEdit()
        layout.addWidget(tedit)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
