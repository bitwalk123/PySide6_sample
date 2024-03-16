from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QFrame,
    QLabel,
)


class MyDockWidget(QDockWidget):
    def __init__(self, title: str, side: str):
        super().__init__()
        self.setWindowTitle(title)

        base = QLabel('Dock')
        base.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if side == 'leftright':
            base.setFixedWidth(80)
        elif side == 'topbottom':
            base.setFixedHeight(50)

        base.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        base.setLineWidth(1)
        self.setWidget(base)
