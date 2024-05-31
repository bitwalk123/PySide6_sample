import os
import sys
from os.path import expanduser

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class WatchDog(QObject, FileSystemEventHandler):
    onAnyEvent = Signal(str)

    def __init__(self):
        super().__init__()

    def on_any_event(self, e):
        msg = '%s : %s : %s' % (
            str(e.is_directory),
            e.event_type,
            e.src_path
        )
        self.onAnyEvent.emit(msg)


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
        dog.onAnyEvent.connect(self.update_output)
        observer = Observer()
        observer.schedule(dog, path=dir_target, recursive=True)
        observer.start()

    def update_output(self, msg: str):
        self.output.insertPlainText(msg + '\n')
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
