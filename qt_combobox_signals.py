import sys

from PySide6.QtCore import QMargins
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QComboBox')

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(vbox)

        combo = QComboBox()
        combo.setFixedWidth(200)
        combo.setEditable(True)
        combo.activated.connect(self.on_activated)
        combo.currentIndexChanged.connect(self.on_current_index_changed)
        combo.currentTextChanged.connect(self.on_current_text_changed)
        combo.editTextChanged.connect(self.on_edit_text_changed)
        combo.highlighted.connect(self.on_highlighted)
        combo.textActivated.connect(self.on_text_activated)
        combo.textHighlighted.connect(self.on_text_highlighted)
        vbox.addWidget(combo)

    @staticmethod
    def on_activated(*args):
        print('activated', *args)

    @staticmethod
    def on_current_index_changed(*args):
        print('currentIndexChanged', *args)

    @staticmethod
    def on_current_text_changed(*args):
        print('currentTextChanged', *args)

    @staticmethod
    def on_edit_text_changed(*args):
        print('editTextChanged', *args)

    @staticmethod
    def on_highlighted(*args):
        print('highlighted', *args)

    @staticmethod
    def on_text_activated(*args):
        print('textActivated', *args)

    @staticmethod
    def on_text_highlighted(*args):
        print('textHighlighted', *args)


def main():
    app: QApplication = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
