from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QStatusBar,
)


class MyStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setSizeGripEnabled(True)
        lab = QLabel("StatusBar")
        lab.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        lab.setLineWidth(1)
        lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.addWidget(lab, stretch=1)
