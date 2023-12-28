from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Entry(QLineEdit):
    def __init__(self, key: str):
        super().__init__()
        self.key: str = key
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        self.setStyleSheet("QLineEdit{background-color:white;}")

    def getKey(self) -> str:
        return self.key


class DBInfoDlg(QDialog):
    def __init__(self, dict_info: dict):
        super().__init__()
        self.dict_info = dict_info
        self.setWindowTitle('DB Info')

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(vbox)

        base = QWidget()
        self.gen_entries(base)
        vbox.addWidget(base)

        dlgbtn = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlgbtn)
        bbox.accepted.connect(self.accept)
        vbox.addWidget(bbox)

    def gen_entries(self, base):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        base.setLayout(layout)

        for row, key in enumerate(['host', 'database', 'user', 'password']):
            if key == 'password':
                self.gen_row(layout, key, row, True)
            else:
                self.gen_row(layout, key, row)

        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)

    def gen_row(self, grid: QGridLayout, key: str, row: int, flag: int = False):
        lab = QLabel(key)
        lab.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        lab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        grid.addWidget(lab, row, 0)

        ent = Entry(key)
        if flag:
            ent.setEchoMode(QLineEdit.EchoMode.Password)
        ent.textChanged.connect(self.entry_changed)
        grid.addWidget(ent, row, 1)

    def entry_changed(self, content: str):
        ent: Entry = self.sender()
        key = ent.getKey()
        self.dict_info[key] = content
