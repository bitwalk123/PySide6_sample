import sys
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit")

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        entry = QLineEdit()
        entry.returnPressed.connect(self.on_entry_entered)
        entry.setMinimumWidth(200)
        entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        vbox.addWidget(entry)

    def on_entry_entered(self):
        lineedit: QLineEdit = self.sender()
        print('「' + lineedit.text() + '」が入力されました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
