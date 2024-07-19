import sys

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar, QToolButton, QStyle, QLineEdit, QFileDialog, QStatusBar, QLabel,
)

"""
def main():
    app = QGuiApplication(sys.argv)

    filename = 'cat1.wav'
    effect = QSoundEffect()
    effect.setSource(QUrl.fromLocalFile(filename))
    # possible bug: QSoundEffect::Infinite cannot be used in setLoopCount
    effect.setLoopCount(-2)
    effect.play()

    sys.exit(app.exec())
"""


class MyToolBar(QToolBar):
    mediaPlay = Signal(str)
    mediaStop = Signal()

    def __init__(self):
        super().__init__()

        but_folder = QToolButton()
        ico_folder = self.get_icon('SP_DirIcon')
        but_folder.setIcon(ico_folder)
        but_folder.clicked.connect(self.file_dialog)
        self.addWidget(but_folder)

        self.but_play = but_play = QToolButton()
        ico_play = self.get_icon('SP_MediaPlay')
        but_play.setIcon(ico_play)
        but_play.setEnabled(False)
        but_play.clicked.connect(self.wav_play)
        self.addWidget(but_play)

        self.but_stop = but_stop = QToolButton()
        ico_stop = self.get_icon('SP_MediaStop')
        but_stop.setIcon(ico_stop)
        but_stop.setEnabled(False)
        but_stop.clicked.connect(self.wav_stop)
        self.addWidget(but_stop)

        self.addSeparator()

        self.entry = entry = QLineEdit()
        entry.setStyleSheet("""
            QLineEdit {margin-left: 5; padding: 0 5 0 5;}
            QLineEdit:disabled {background-color: white;}
        """)
        entry.setEnabled(False)
        self.addWidget(entry)

    def file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter('wav file (*.wav)')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.entry.setText(filename)
            self.but_play.setEnabled(True)

    def get_icon(self, name: str) -> QIcon:
        pixmap = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap)
        return icon

    def wav_play(self):
        self.playStart()
        self.mediaPlay.emit(self.entry.text())

    def wav_stop(self):
        self.playEnd()
        self.mediaStop.emit()

    def playStart(self):
        self.but_play.setEnabled(False)
        self.but_stop.setEnabled(True)

    def playEnd(self):
        self.but_play.setEnabled(True)
        self.but_stop.setEnabled(False)


class MyStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.lab = lab = QLabel()
        self.addWidget(lab, stretch=True)

    def addMSG(self, msg: str):
        self.lab.setText(msg)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wav Player')

        self.toolbar = toolbar = MyToolBar()
        toolbar.mediaPlay.connect(self.sound_play)
        toolbar.mediaStop.connect(self.sound_stop)
        self.addToolBar(toolbar)

        self.statusbar = statusbar = MyStatusBar()
        self.setStatusBar(statusbar)

        self.effect = QSoundEffect()
        self.effect.statusChanged.connect(self.status_changed)
        self.effect.loopsRemainingChanged.connect(self.remaining_changed)

    def remaining_changed(self):
        if self.effect.loopsRemaining() == 0:
            self.toolbar.playEnd()

    def status_changed(self):
        if self.effect.status() == QSoundEffect.Status.Loading:
            msg = 'Loading'
        elif self.effect.status() == QSoundEffect.Status.Ready:
            msg = 'Ready'
        elif self.effect.status() == QSoundEffect.Status.Error:
            msg = 'Error'
        elif self.effect.status() == QSoundEffect.Status.Null:
            msg = 'Null'
        else:
            msg = 'Unknown'

        self.statusbar.addMSG(msg)

    def sound_play(self, wav_file: str):
        self.effect.setSource(QUrl.fromLocalFile(wav_file))
        # self.effect.setLoopCount(-2)
        self.effect.play()

    def sound_stop(self):
        self.effect.stop()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
