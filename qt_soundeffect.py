import sys

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication,
    QDial,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QStatusBar,
    QStyle,
    QToolBar,
    QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGridLayout,
)


def get_icon(parent, name: str) -> QIcon:
    pixmap = getattr(QStyle.StandardPixmap, name)
    icon = parent.style().standardIcon(pixmap)
    return icon


class MyToolBar(QToolBar):
    wavSelected = Signal(str)
    wavPlay = Signal()
    wavStop = Signal()
    wavVolume = Signal(float)

    def __init__(self):
        super().__init__()

        but_folder = QToolButton()
        ico_folder = get_icon(self, 'SP_DirIcon')
        but_folder.setIcon(ico_folder)
        but_folder.clicked.connect(self.file_dialog)
        self.addWidget(but_folder)

        self.but_play = but_play = QToolButton()
        ico_play = get_icon(self, 'SP_MediaPlay')
        but_play.setIcon(ico_play)
        but_play.setEnabled(False)
        but_play.clicked.connect(self.wav_play)
        self.addWidget(but_play)

        self.but_stop = but_stop = QToolButton()
        ico_stop = get_icon(self, 'SP_MediaStop')
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

        self.dial = dial = QDial()
        dial.setFixedSize(32, 32)
        dial.setMinimum(0)
        dial.setMaximum(100)
        dial.setValue(25)
        dial.valueChanged.connect(self.change_dial)
        self.addWidget(dial)

    def change_dial(self, value: int):
        self.wavVolume.emit(value / 100.)

    def file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter('wav file (*.wav)')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.but_play.setEnabled(True)
            self.entry.setText(filename)
            self.wavSelected.emit(filename)

    def getVolume(self):
        return self.dial.value() / 100.

    def wav_play(self):
        self.playStart()
        self.wavPlay.emit()

    def wav_stop(self):
        self.playEnd()
        self.wavStop.emit()

    def playStart(self):
        self.but_play.setEnabled(False)
        self.but_stop.setEnabled(True)

    def playEnd(self):
        self.but_play.setEnabled(True)
        self.but_stop.setEnabled(False)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_win = get_icon(self, 'SP_TitleBarMenuButton')
        self.setWindowIcon(icon_win)
        self.setWindowTitle('Wav Player')
        self.effect = None

        self.toolbar = toolbar = MyToolBar()
        toolbar.wavSelected.connect(self.source_selected)
        toolbar.wavPlay.connect(self.sound_play)
        toolbar.wavStop.connect(self.sound_stop)
        toolbar.wavVolume.connect(self.set_volume)
        self.addToolBar(toolbar)

        self.pte = pte = QPlainTextEdit()
        pte.setReadOnly(True)
        pte.setStyleSheet("""
            QPlainTextEdit {background-color: white;}
        """)

        self.setCentralWidget(pte)

    def add_msg(self, msg: str):
        # Reference:
        # https://stackoverflow.com/questions/14550146/qtextedit-scroll-down-automatically-only-if-the-scrollbar-is-at-the-bottom
        scr = self.pte.verticalScrollBar()
        scr_at_bottom = (scr.value() >= (scr.maximum() - 4))
        scr_prev_value = scr.value()

        self.pte.insertPlainText('%s\n' % msg)

        if scr_at_bottom:
            self.pte.ensureCursorVisible()
        else:
            self.pte.verticalScrollBar().setValue(scr_prev_value)

    def create_sound_effect(self, wav_file: str):
        self.effect = QSoundEffect()
        self.effect.loopsRemainingChanged.connect(self.remaining_changed)
        self.effect.sourceChanged.connect(self.source_changed)
        self.effect.statusChanged.connect(self.status_changed)
        self.effect.volumeChanged.connect(self.volume_changed)

        self.effect.setSource(QUrl.fromLocalFile(wav_file))
        self.effect.setVolume(self.toolbar.getVolume())

    def remaining_changed(self):
        if self.effect.loopsRemaining() == 0:
            qurl: QUrl = self.effect.source()
            msg = 'End playing "%s".' % qurl.fileName()
            self.add_msg(msg)
            self.toolbar.playEnd()

    def set_volume(self, volume: float):
        if self.effect is not None:
            self.effect.setVolume(volume)

    def source_changed(self):
        qurl: QUrl = self.effect.source()
        self.add_msg('Wav file: %s' % qurl.fileName())

    def source_selected(self, wav_file: str):
        self.create_sound_effect(wav_file)

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

        self.add_msg(msg)

    def sound_play(self):
        qurl: QUrl = self.effect.source()
        msg = 'Start playing "%s".' % qurl.fileName()
        self.add_msg(msg)
        self.effect.play()

    def sound_stop(self):
        qurl: QUrl = self.effect.source()
        msg = 'Stop playing "%s".' % qurl.fileName()
        self.add_msg(msg)
        self.effect.stop()

    def volume_changed(self):
        msg = 'Volume: %.2f' % self.effect.volume()
        self.add_msg(msg)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
