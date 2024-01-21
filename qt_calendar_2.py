#!/usr/bin/env python
# coding: utf-8

import sys

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QLineEdit,
    QMainWindow,
    QStyle,
    QToolBar,
    QToolButton,
)


class DateEntry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.qdate: QDate | None = None
        self.setEnabled(False)

    def getDate(self) -> QDate | None:
        return self.qdate

    def setDate(self, qdate: QDate):
        self.qdate = qdate
        self.setText('{:0=4}-{:0=2}-{:0=2}'.format(
            qdate.year(), qdate.month(), qdate.day()
        ))


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calendar: QCalendarWidget | None = None

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.entry = DateEntry()
        toolbar.addWidget(self.entry)

        but_calendar = QToolButton()
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        but_calendar.setIcon(icon)
        but_calendar.clicked.connect(self.on_clicked)
        toolbar.addWidget(but_calendar)

    def on_date_selected(self, qdate: QDate):
        self.entry.setDate(qdate)
        if self.calendar is not None:
            self.calendar.hide()
            self.calendar.deleteLater()

    def on_clicked(self):
        self.calendar = QCalendarWidget()
        qdate = self.entry.getDate()
        if qdate is not None:
            self.calendar.setSelectedDate(qdate)
        self.calendar.activated.connect(self.on_date_selected)
        self.calendar.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
