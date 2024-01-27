#!/usr/bin/env python
# coding: utf-8
import sys

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
)


def main():
    app = QApplication(sys.argv)

    player = QMediaPlayer()
    player.setSource(QUrl.fromLocalFile('big_buck_bunny_720p_1mb.mp4'))
    video = QVideoWidget()
    player.setVideoOutput(video)
    video.show()
    player.play()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
