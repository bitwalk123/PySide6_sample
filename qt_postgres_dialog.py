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


class Label(QLabel):

    def __init__(self, text: str):
        super().__init__(text)
        self.setLineWidth(1)
        self.setFrameStyle(
            QFrame.Shape.StyledPanel | QFrame.Shadow.Raised
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
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
        vbox.setContentsMargins(0, 0, 0, 0)
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
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(1)
        base.setLayout(grid)

        key = 'host'
        row = 0
        self.gen_row(grid, key, row)

        key = 'database'
        row = 1
        self.gen_row(grid, key, row)

        key = 'table'
        row = 2
        self.gen_row(grid, key, row)

        key = 'user'
        row = 3
        self.gen_row(grid, key, row)

        key = 'password'
        row = 4
        self.gen_row(grid, key, row, True)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

    def gen_row(self, grid: QGridLayout, key: str, row: int, flag: int = False):
        lab = Label(key)
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
