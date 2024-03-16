from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QStyle


class OpenToolButton(QToolButton):
    def __init__(self):
        super().__init__()

        bame_open = 'SP_DirOpenIcon'
        icon = self.get_builtin_icon(bame_open)
        self.setIcon(icon)
        self.setStatusTip('Open file')

    def get_builtin_icon(self, name: str) -> QIcon:
        pixmap = getattr(QStyle.StandardPixmap, name)
        return self.style().standardIcon(pixmap)
