import os
import sys
from os.path import expanduser

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
    QWidget,
)
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent
)
from watchdog.observers import Observer


class WatchDog(QObject, FileSystemEventHandler):
    fileCreated = Signal(FileCreatedEvent)

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        self.fileCreated.emit(event)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WatchDog test')

        dir_target = os.path.join(expanduser("~"), 'tmp')
        if not os.path.exists(dir_target):
            os.mkdir(dir_target)

        self.output = output = QPlainTextEdit()
        output.setStyleSheet('font-family: monospace;')
        output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        output.setReadOnly(True)
        self.setCentralWidget(output)

        dog = WatchDog()
        dog.fileCreated.connect(self.file_created)
        observer = Observer()
        observer.schedule(dog, path=dir_target, recursive=True)
        observer.start()

    def file_created(self, e: FileCreatedEvent):
        message = '%s is added!\n' % e.src_path
        self.update_output(message)

    def update_output(self, msg: str):
        self.output.insertPlainText(msg)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
