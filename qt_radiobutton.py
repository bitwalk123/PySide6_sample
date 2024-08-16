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
        self.setWindowTitle('QRadioButton')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        rb_a = QRadioButton('ラジオボタンＡ')
        rb_a.toggle()
        vbox.addWidget(rb_a)

        rb_b = QRadioButton('ラジオボタンＢ')
        vbox.addWidget(rb_b)

        rb_c = QRadioButton('ラジオボタンＣ')
        vbox.addWidget(rb_c)

        self.rb_group = rb_group = QButtonGroup()
        rb_group.addButton(rb_a)
        rb_group.addButton(rb_b)
        rb_group.addButton(rb_c)
        rb_group.buttonToggled.connect(self.radiobutton_changed)

    def radiobutton_changed(self, rb: QRadioButton, state: bool):
        if state:
            status = 'オン'
        else:
            status = 'オフ'
        print('「%s」を%sにしました。' % (rb.text(), status))


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
