import sys

from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import (
    QApplication,
    QDial,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QStyle,
    QToolBar,
    QToolButton,
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
        but_folder.setToolTip('Choose wav file.')
        ico_folder = get_icon(self, 'SP_DirIcon')
        but_folder.setIcon(ico_folder)
        but_folder.clicked.connect(self.file_dialog)
        self.addWidget(but_folder)

        self.but_play = but_play = QToolButton()
        but_play.setToolTip('Start playing wav file.')
        ico_play = get_icon(self, 'SP_MediaPlay')
        but_play.setIcon(ico_play)
        but_play.setEnabled(False)
        but_play.clicked.connect(self.wav_play)
        self.addWidget(but_play)

        self.but_stop = but_stop = QToolButton()
        but_stop.setToolTip('Stop playing wav file.')
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
        self.wavVolume.emit(value / 100.)

    def file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Sound files (*.wav *.mp3)')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            self.but_play.setEnabled(True)
            self.entry.setText(filename)
            self.wavSelected.emit(filename)

    def getVolume(self) -> float:
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


class MySoundPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_win = get_icon(self, 'SP_TitleBarMenuButton')
        self.setWindowIcon(icon_win)
        self.setWindowTitle('Sound Player')

        self.toolbar = toolbar = MyToolBar()
        toolbar.wavSelected.connect(self.source_selected)
        toolbar.wavPlay.connect(self.sound_play)
        toolbar.wavStop.connect(self.sound_stop)
        toolbar.wavVolume.connect(self.set_volume)
        self.addToolBar(toolbar)

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
        player.playbackRateChanged.connect(self.playback_rate_changed)
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
        print(duration)

    def playback_rate_changed(self, rate: float):
        print('playback rate', rate)

    def playback_state_changed(self, status):
        print(status)

    def set_volume(self, volume: float):
        self.output.setVolume(volume)

    def source_changed(self):
        qurl: QUrl = self.player.source()
        self.add_msg('Wav file: %s' % qurl.fileName())

    def source_selected(self, file: str):
        self.player.setSource(QUrl.fromLocalFile(file))

    def sound_play(self):
        self.player.play()

    def sound_stop(self):
        self.player.stop()

    def volume_changed(self, volume: float):
        print('Volume', volume)


def main():
    app = QApplication(sys.argv)
    ex = MySoundPlayer()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
