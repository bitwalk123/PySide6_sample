import sys

from PySide6.QtGui import QActionGroup, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QToolBar,
    QToolButton,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbutton = QToolButton()
        toolbutton.setText('Menu')
        toolbar.addWidget(toolbutton)

        toolmenu = QMenu(self)
        toolbutton.setMenu(toolmenu)
        toolbutton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )
        group_action = QActionGroup(self)

        action_1 = QAction('Action 1')
        action_1.setCheckable(True)
        action_1.toggled.connect(self.on_toggled)
        toolmenu.addAction(action_1)
        group_action.addAction(action_1)

        action_2 = QAction('Action 2')
        action_2.setCheckable(True)
        action_2.toggled.connect(self.on_toggled)
        toolmenu.addAction(action_2)
        group_action.addAction(action_2)

        action_3 = QAction('Action 3')
        action_3.setCheckable(True)
        action_3.toggled.connect(self.on_toggled)
        toolmenu.addAction(action_3)
        group_action.addAction(action_3)

    def on_toggled(self):
        action: QAction = self.sender()
        if action.isChecked():
            print(action.text(), 'is selected.')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
