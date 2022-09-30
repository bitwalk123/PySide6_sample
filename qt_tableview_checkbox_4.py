# Reference:
# https://www.pythonfixing.com/2022/03/fixed-update-object-when-checkbox.html
import os
import sys
import random

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class PlayblastJob(object):
    def __init__(self, **kwargs):
        super(PlayblastJob, self).__init__()

        # instance properties
        self.active = True
        self.name = ''
        self.camera = ''
        self.renderWidth = 1920
        self.renderHeight = 1080
        self.renderScale = 1.0
        self.status = ''

        # initialize attribute values
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def getScaledRenderSize(self):
        x = int(self.renderWidth * self.renderScale)
        y = int(self.renderHeight * self.renderScale)
        return (x, y)


class JobModel(QAbstractTableModel):
    HEADERS = ['Name', 'Camera', 'Resolution', 'Status']

    def __init__(self):
        super(JobModel, self).__init__()
        self.items = []

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.HEADERS[section]
        return None

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def appendJob(self, *items):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1)
        for item in items:
            assert isinstance(item, PlayblastJob)
            self.items.append(item)
        self.endInsertRows()

    def removeJobs(self, items):
        rowsToRemove = []
        for row, item in enumerate(self.items):
            if item in items:
                rowsToRemove.append(row)
        for row in sorted(rowsToRemove, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.items.pop(row)
            self.endRemoveRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
        self.items = []
        self.endRemoveRows()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return

        row = index.row()
        col = index.column()

        if 0 <= row < self.rowCount():
            item = self.items[row]
            if role == Qt.DisplayRole:
                if col == 0:
                    return item.name
                elif col == 1:
                    return item.camera
                elif col == 2:
                    width, height = item.getScaledRenderSize()
                    return '{} x {}'.format(width, height)
                elif col == 3:
                    return item.status.title()
            elif role == Qt.ForegroundRole:
                if col == 3:
                    if item.status == 'error':
                        return QColor(255, 82, 82)
                    elif item.status == 'success':
                        return QColor(76, 175, 80)
                    elif item.status == 'warning':
                        return QColor(255, 193, 7)
            elif role == Qt.TextAlignmentRole:
                if col == 2:
                    return Qt.AlignCenter
                if col == 3:
                    return Qt.AlignCenter
            elif role == Qt.CheckStateRole:
                if col == 0:
                    if item.active:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
            elif role == Qt.UserRole:
                return item
        return None


class JobQueue(QWidget):
    '''
    Description:
        Widget that manages the Jobs Queue
    '''

    def __init__(self):
        super(JobQueue, self).__init__()
        self.resize(400, 600)

        # controls
        self.uiAddNewJob = QPushButton('Add New Job')
        self.uiAddNewJob.setToolTip('Add new job')

        self.uiRemoveSelectedJobs = QPushButton('Remove Selected')
        self.uiRemoveSelectedJobs.setToolTip('Remove selected jobs')

        self.jobModel = JobModel()
        self.uiJobTableView = QTableView()
        self.uiJobTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uiJobTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.uiJobTableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.uiJobTableView.setModel(self.jobModel)

        self.jobSelection = self.uiJobTableView.selectionModel()

        self.uiRandomize = QPushButton('Randomize Selected Values')
        self.uiPrintJobs = QPushButton('Print Jobs')

        # sub layouts
        self.jobQueueToolsLayout = QHBoxLayout()
        self.jobQueueToolsLayout.addWidget(self.uiAddNewJob)
        self.jobQueueToolsLayout.addWidget(self.uiRemoveSelectedJobs)
        self.jobQueueToolsLayout.addStretch()
        self.jobQueueToolsLayout.addWidget(self.uiRandomize)

        # layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.jobQueueToolsLayout)
        self.mainLayout.addWidget(self.uiJobTableView)
        self.mainLayout.addWidget(self.uiPrintJobs)
        self.setLayout(self.mainLayout)

        # connections
        self.uiAddNewJob.clicked.connect(self.addNewJob)
        self.uiRemoveSelectedJobs.clicked.connect(self.removeSelectedJobs)
        self.uiRandomize.clicked.connect(self.randomizeSelected)
        self.uiPrintJobs.clicked.connect(self.printJobs)

    # methods
    def addNewJob(self):
        name = random.choice(['Kevin', 'Melissa', 'Suzie', 'Eddie', 'Doug'])
        job = PlayblastJob(name=name, camera='Camera001', startFrame=50)
        self.jobModel.appendJob(job)

    def removeSelectedJobs(self):
        jobs = self.getSelectedJobs()
        self.jobModel.removeJobs(jobs)

    def getSelectedJobs(self):
        jobs = [x.data(Qt.UserRole) for x in self.jobSelection.selectedRows()]
        return jobs

    def randomizeSelected(self):
        jobs = self.getSelectedJobs()
        for job in jobs:
            job.camera = random.choice(['Canon', 'Nikon', 'Sony', 'Red'])
            job.status = random.choice(['error', 'warning', 'success'])

    def printJobs(self):
        jobs = self.jobModel.items
        for job in jobs:
            print(vars(job))


def main():
    app = QApplication(sys.argv)
    window = JobQueue()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
