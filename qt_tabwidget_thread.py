import sys

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
)
from PySide6.QtGui import QGuiApplication, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QWidget,
)


class Tab1Widget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        button = QPushButton('Click Me!')
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(self.hello)
        hbox = QHBoxLayout()
        hbox.addWidget(button)
        self.setLayout(hbox)

    def hello(self):
        print('Hello!')


class TabWorker(QObject):
    tabCompleted = Signal()
    finished = Signal()

    page: dict = None
    widget = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @Slot()
    def run(self):
        self.widget = Tab1Widget(self.parent)
        self.page = page = {'0': self.widget}
        self.tabCompleted.emit()
        self.finished.emit()

    def getPage(self):
        return self.page

    def getWidget(self):
        return self.widget


class Example(QMainWindow):
    tab: QTabWidget = None
    tabber: TabWorker = None
    thread_tabber: QThread = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QTabWidget')
        self.resize(400, 400)

    def init_ui(self):
        self.tab = tab = QTabWidget()
        self.setCentralWidget(tab)
        self.add_tab()

    def add_tab(self):
        # Prep. Threading
        self.tabber = TabWorker(self)
        self.thread_tabber = QThread()
        self.tabber.moveToThread(self.thread_tabber)
        # Controller
        self.thread_tabber.started.connect(self.tabber.run)
        self.tabber.finished.connect(self.thread_tabber.quit)
        # self.tabber.finished.connect(self.tabber.deleteLater)
        # self.thread_tabber.finished.connect(self.thread_tabber.deleteLater)
        self.tabber.tabCompleted.connect(self.add_tab_completed)
        # Start Threading
        self.thread_tabber.start()

    def add_tab_completed(self):
        mainThread = QGuiApplication.instance().thread()
        self.tabber.moveToThread(mainThread)
        obj = self.tabber.getWidget()
        print(type(obj), type(Tab1Widget(self)))
        obj.setParent(self)
        self.tab.addTab(obj, 'Tab0')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
