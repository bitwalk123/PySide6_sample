from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MyMenuBar(QMenuBar):
    openTriggered = Signal()
    exitTriggered = Signal()

    def __init__(self):
        super().__init__()
        menu_file = self.addMenu('&File')
        menu_edit = self.addMenu('&Edit')

        action_open = QAction('&Open', self)
        action_open.setStatusTip('Open file')
        action_open.triggered.connect(self.on_triggered_open)
        menu_file.addAction(action_open)

        action_exit = QAction('E&xit', self)
        action_exit.setStatusTip('Exit app')
        action_exit.triggered.connect(self.on_triggered_exit)
        menu_file.addAction(action_exit)

        action_cut = QAction('Cu&t', self)
        action_cut.setStatusTip('Cut')
        menu_edit.addAction(action_cut)

        action_copy = QAction('&Copy', self)
        action_copy.setStatusTip('Copy')
        menu_edit.addAction(action_copy)

        action_paste = QAction('&Paste', self)
        action_paste.setStatusTip('Paste')
        menu_edit.addAction(action_paste)

    def on_triggered_open(self):
        self.openTriggered.emit()

    def on_triggered_exit(self):
        self.exitTriggered.emit()
