from PySide6.QtWidgets import QPushButton


class Plugin(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText('Plugin Test 2')
