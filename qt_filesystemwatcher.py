import os
import sys
from os.path import expanduser

from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FileSystemWatcher')
        dir_target = os.path.join(expanduser("~"), 'tmp')
        if not os.path.exists(dir_target):
            os.mkdir(dir_target)

        self.watcher = watcher = QFileSystemWatcher()
        watcher.addPath(dir_target)
        watcher.directoryChanged.connect(self.directory_changed)

        self.out = out = QPlainTextEdit()
        out.setStyleSheet('font-family: monospace;')
        out.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        out.setReadOnly(True)
        self.setCentralWidget(out)

    def directory_changed(self, path: str):
        self.out.insertPlainText('%s is changed!\n' % path)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
