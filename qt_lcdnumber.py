import datetime
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLCDNumber, QVBoxLayout


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 50)
        self.setWindowTitle('Clock')

        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(box)

        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.lcd.display('00:00:00')
        box.addWidget(self.lcd)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

    def update_time(self):
        dt_now = datetime.datetime.now()
        self.lcd.display(dt_now.strftime('%H:%M:%S'))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
