#!/usr/bin/env python
# coding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog


class EndlessProgressDialog(QProgressDialog):
    def __init__(self, parent):
        super().__init__(labelText='Working...', parent=parent)
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.setRange(0, 0)
        self.setWindowTitle('in progress')
