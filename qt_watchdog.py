import os
import sys
from os.path import expanduser

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Example(QMainWindow, FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WatchDog')
        dir_target = os.path.join(expanduser("~"), 'tmp')
        if not os.path.exists(dir_target):
            os.mkdir(dir_target)

        lab = QLabel('THis is for WatchDog test')
        self.setCentralWidget(lab)

        observer = Observer()
        observer.schedule(
            self,
            path=dir_target,
            recursive=True
        )
        observer.start()

    def on_any_event(self, e):
        print(f"{e.is_directory} : {e.event_type} : {e.src_path}")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
