import sys

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QWidget,
)


class Example(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.init_ui()
        self.setWindowTitle('Standard Location')

    def init_ui(self):
        base = QWidget()
        base.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.setWidget(base)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        base.setLayout(layout)

        names = sorted(
            [attr for attr in dir(QStandardPaths.StandardLocation) if not attr.startswith('__')]
        )
        row = 0
        for name in names:
            enum_stdloc = getattr(QStandardPaths.StandardLocation, name)
            list_loc = QStandardPaths.standardLocations(enum_stdloc)
            span = len(list_loc)

            label_name = QLabel(name)
            label_name.setFrameStyle(
                QFrame.Shape.StyledPanel | QFrame.Shadow.Raised
            )
            label_name.setLineWidth(2)
            label_name.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Expanding
            )
            label_name.setStyleSheet("""
                QLabel {
                    padding:0.1em 0.2em;
                }
            """)
            layout.addWidget(label_name, row, 0, span, 1)

            for idx, loc in enumerate(list_loc):
                label_value = QLabel(loc)
                label_value.setFrameStyle(
                    QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken
                )
                label_value.setLineWidth(2)
                label_value.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Expanding
                )
                label_value.setStyleSheet("""
                    QLabel {
                        padding:0.1em 0.2em;
                        background-color:white;
                    }
                """)
                layout.addWidget(label_value, row + idx, 1, 1, 1)

            row += span


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
