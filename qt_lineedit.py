import sys
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit")

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        lab = QLabel('Name:')
        lab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox.addWidget(lab)

        entry = QLineEdit()
        entry.returnPressed.connect(self.on_entry_entered)
        entry.setMinimumWidth(200)
        entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox.addWidget(entry)

    def on_entry_entered(self):
        lineedit: QLineEdit = self.sender()
        print('Your name: ' + lineedit.text())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
