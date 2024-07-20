import sys

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QDial,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QStatusBar,
    QStyle,
    QToolBar,
    QToolButton,
)


def get_icon(parent, name: str) -> QIcon:
    pixmap = getattr(QStyle.StandardPixmap, name)
    icon = parent.style().standardIcon(pixmap)
    return icon


class MyToolBar(QToolBar):
    soundSelected = Signal(str)
    soundPlay = Signal()
    soundStop = Signal()
    soundVolume = Signal(float)

    def __init__(self):
        super().__init__()

        but_folder = QToolButton()
        but_folder.setToolTip('Choose sound file.')
        ico_folder = get_icon(self, 'SP_DirIcon')
        but_folder.setIcon(ico_folder)
        but_folder.clicked.connect(self.file_dialog)
        self.addWidget(but_folder)

        self.but_play = but_play = QToolButton()
        but_play.setToolTip('Start playing sound file.')
        ico_play = get_icon(self, 'SP_MediaPlay')
        but_play.setIcon(ico_play)
        but_play.setEnabled(False)
        but_play.clicked.connect(self.wav_play)
        self.addWidget(but_play)

        self.but_stop = but_stop = QToolButton()
        but_stop.setToolTip('Stop playing sound file.')
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
        dial.setToolTip('Adjust sound volume.')
        dial.setFixedSize(32, 32)
        dial.setMinimum(0)
        dial.setMaximum(100)
        dial.setValue(25)
        dial.valueChanged.connect(self.change_dial)
        self.addWidget(dial)

    def change_dial(self, value: int):
        self.soundVolume.emit(value / 100.)

    def file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Sound files (*.wav *.mp3)')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.but_play.setEnabled(True)
            self.entry.setText(filename)
            self.soundSelected.emit(filename)

    def getVolume(self) -> float:
        return self.dial.value() / 100.

    def wav_play(self):
        self.playStart()
        self.soundPlay.emit()

    def wav_stop(self):
        self.playEnd()
        self.soundStop.emit()

    def playStart(self):
        self.but_play.setEnabled(False)
        self.but_stop.setEnabled(True)

    def playEnd(self):
        self.but_play.setEnabled(True)
        self.but_stop.setEnabled(False)


class MyStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.progress = progress = QProgressBar()
        self.addWidget(progress, stretch=True)

    def clearProgress(self):
        self.setProgress(0)

    def setDuration(self, maximum: int):
        self.progress.setRange(0, maximum)

    def setProgress(self, progress: int):
        self.progress.setValue(progress)


class MySoundPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_win = get_icon(self, 'SP_TitleBarMenuButton')
        self.setWindowIcon(icon_win)
        self.setWindowTitle('Sound Player')

        self.toolbar = toolbar = MyToolBar()
        toolbar.soundSelected.connect(self.source_selected)
        toolbar.soundPlay.connect(self.sound_play)
        toolbar.soundStop.connect(self.sound_stop)
        toolbar.soundVolume.connect(self.set_volume)
        self.addToolBar(toolbar)

        self.statusbar = statusbar = MyStatusBar()
        self.setStatusBar(statusbar)

        self.pte = pte = QPlainTextEdit()
        pte.setReadOnly(True)
        pte.setStyleSheet('QPlainTextEdit {background-color: white;}')
        self.setCentralWidget(pte)

        self.output = output = QAudioOutput()
        output.setVolume(toolbar.getVolume())
        output.volumeChanged.connect(self.volume_changed)

        self.player = player = QMediaPlayer()
        player.setAudioOutput(output)
        player.durationChanged.connect(self.duration_changed)
        player.positionChanged.connect(self.position_changed)
        player.playbackStateChanged.connect(self.playback_state_changed)
        player.sourceChanged.connect(self.source_changed)

    def add_msg(self, msg: str):
        scr = self.pte.verticalScrollBar()
        scr_at_bottom = (scr.value() >= (scr.maximum() - 4))
        scr_prev_value = scr.value()

        self.pte.insertPlainText('%s\n' % msg)

        if scr_at_bottom:
            self.pte.ensureCursorVisible()
        else:
            self.pte.verticalScrollBar().setValue(scr_prev_value)

    def duration_changed(self, duration: int):
        self.statusbar.setDuration(duration)

    def position_changed(self, position: int):
        self.statusbar.setProgress(position)

    def playback_state_changed(self, status: QMediaPlayer.PlaybackState):
        if status == QMediaPlayer.PlaybackState.PausedState:
            self.add_msg('Paused')
        elif status == QMediaPlayer.PlaybackState.PlayingState:
            self.add_msg('Playing')
        elif status == QMediaPlayer.PlaybackState.StoppedState:
            self.statusbar.clearProgress()
            self.add_msg('Stopped')
        else:
            self.add_msg('Unknown status')

    def set_volume(self, volume: float):
        self.output.setVolume(volume)

    def source_changed(self):
        qurl: QUrl = self.player.source()
        self.add_msg('Sound file: %s' % qurl.fileName())

    def source_selected(self, file: str):
        self.player.setSource(QUrl.fromLocalFile(file))

    def sound_play(self):
        self.player.play()

    def sound_stop(self):
        self.player.stop()

    def volume_changed(self, volume: float):
        self.add_msg('Volume = %.2f' % volume)


def main():
    app = QApplication(sys.argv)
    ex = MySoundPlayer()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
