import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QWidget,
)


class Tab1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(parent.close)
        hbox = QHBoxLayout()
        hbox.addWidget(closeBtn)
        self.setLayout(hbox)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('QTabWidget')
        self.resize(400, 400)
        self.show()

    def init_ui(self):
        tab = QTabWidget()
        tab.addTab(Tab1Widget(parent=self), 'Tab1')
        tab.addTab(QLabel('Label 2'), 'Tab2')

        hbox = QHBoxLayout()
        hbox.addWidget(tab)

        self.setLayout(hbox)


def main():
    app = QApplication(sys.argv)
    ui = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()