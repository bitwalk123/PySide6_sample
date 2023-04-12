import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


class Hello(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton("Hello World!", self)
        button.clicked.connect(self.print_hello)
        self.setCentralWidget(button)

    def print_hello(self):
        print("Hello World!")


def main():
    app = QApplication(sys.argv)
    hello = Hello()
    hello.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
