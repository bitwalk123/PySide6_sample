# Reference:
# https://stackoverflow.com/questions/9712461/pyside-wait-for-signal-from-main-thread-in-a-worker-thread
import sys

from PySide6.QtCore import (
    QMutex,
    QThread,
    QWaitCondition,
)
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
)

waitCondition = QWaitCondition()
mutex = QMutex()


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__()

        self.text = QLineEdit()
        self.text.returnPressed.connect(self.wakeup)

        self.worker = Worker(self)
        self.worker.start()

        self.setCentralWidget(self.text)

    def wakeup(self):
        waitCondition.wakeAll()


class Worker(QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

    def run(self):
        print("initial stuff")

        mutex.lock()
        waitCondition.wait(mutex)
        mutex.unlock()

        print("after returnPressed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec())
