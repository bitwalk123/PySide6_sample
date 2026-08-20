from PySide6.QtWidgets import QStyle, QToolButton


class OpenToolButton(QToolButton):
    def __init__(self):
        super().__init__()
        name_open = QStyle.StandardPixmap.SP_DirOpenIcon
        icon = self.style().standardIcon(name_open)
        self.setIcon(icon)
        self.setStatusTip("Open file")
