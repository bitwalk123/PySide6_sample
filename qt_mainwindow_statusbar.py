from PySide6.QtWidgets import QStatusBar


class MyStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setSizeGripEnabled(True)
