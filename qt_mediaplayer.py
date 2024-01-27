#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow

from qt_mediaplayer_toolbar import MyToolBar, get_icon


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.init_audio()
        self.init_video()

        self.setWindowIcon(get_icon(self, 'SP_TitleBarMenuButton'))
        self.setWindowTitle('Media Player')
        self.resize(600, 400)

    def init_audio(self):
        audio = QAudioOutput(self)
        self.player.setAudioOutput(audio)
        audio.setVolume(50)

    def init_video(self):
        toolbar = MyToolBar()
        toolbar.readVideo.connect(self.on_read_video)
        toolbar.playVideo.connect(self.on_play_video)
        self.addToolBar(toolbar)

        video = QVideoWidget(self)
        self.player.setVideoOutput(video)
        self.setCentralWidget(video)

    def on_read_video(self, filename: str):
        self.player.setSource(QUrl.fromLocalFile(filename))

    def on_play_video(self):
        self.player.play()


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
