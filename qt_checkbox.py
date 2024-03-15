import sys
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QCheckBox')

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        cbox_a = QCheckBox('チェックボックスＡ')
        cbox_a.toggle()
        cbox_a.stateChanged.connect(self.checkbox_changed)
        vbox.addWidget(cbox_a)

        cbox_b = QCheckBox('チェックボックスＢ')
        cbox_b.stateChanged.connect(self.checkbox_changed)
        vbox.addWidget(cbox_b)

        cbox_c = QCheckBox('チェックボックスＣ')
        cbox_c.stateChanged.connect(self.checkbox_changed)
        vbox.addWidget(cbox_c)

    def checkbox_changed(self, state):
        cbox = self.sender()
        if cbox.isChecked():
            print('「' + cbox.text() + '」にチェックを入れました。')
        else:
            print('「' + cbox.text() + '」のチェックを外しました。')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
