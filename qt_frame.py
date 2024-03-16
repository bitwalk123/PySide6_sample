import sys
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QFrame')

        layout = QVBoxLayout()
        self.setLayout(layout)

        frm = QFrame()
        frm.setFixedSize(200, 200)
        frm.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        frm.setLineWidth(5)
        layout.addWidget(frm)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
