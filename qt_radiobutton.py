import sys
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RadioButton')

        rb_group = QButtonGroup()

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        rb_a = QRadioButton('ラジオボタンＡ')
        rb_a.toggle()
        rb_a.toggled.connect(self.radiobutton_changed)
        rb_group.addButton(rb_a)
        vbox.addWidget(rb_a)

        rb_b = QRadioButton('ラジオボタンＢ')
        rb_b.toggled.connect(self.radiobutton_changed)
        rb_group.addButton(rb_b)
        vbox.addWidget(rb_b)

        rb_c = QRadioButton('ラジオボタンＣ')
        rb_c.toggled.connect(self.radiobutton_changed)
        rb_group.addButton(rb_c)
        vbox.addWidget(rb_c)

    def radiobutton_changed(self, state):
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            print('「' + rb.text() + '」をオンにしました。')
        else:
            print('「' + rb.text() + '」をオフにしました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
