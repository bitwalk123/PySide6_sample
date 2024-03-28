import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)


class WizardPage(QWizardPage):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap('background.jpeg')
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap, pixmap)


class PageInstallPath(WizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('ようこそインストーラへ')

        self.setSubTitle('インストーラは下記のディレクトリへアプリケーションをインストールします。')
        layout = QVBoxLayout()
        self.setLayout(layout)

        lab = QLabel('インストール先：')
        layout.addWidget(lab)

        ledit = QLineEdit()
        path = os.path.join(os.path.expanduser('~'), 'apps')
        ledit.setText(path)
        ledit.setReadOnly(True)
        layout.addWidget(ledit)


class PageReadyToInstall(WizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('インストール概略')
        self.setSubTitle('「install」ボタンをクリックするとインストールが始まります。')
        self.setCommitPage(True)
        self.setButtonText(QWizard.WizardButton.CommitButton, 'Install')

        layout = QVBoxLayout()
        self.setLayout(layout)


class PageCompleteInstall(WizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('インストール完了')
        self.setSubTitle('アプリケーションのインストールが終了しました。')

        layout = QVBoxLayout()
        self.setLayout(layout)


class Example(QWizard):
    def __init__(self):
        super().__init__()
        self.addPage(PageInstallPath())
        self.addPage(PageReadyToInstall())
        self.addPage(PageCompleteInstall())
        self.setWindowTitle('インストーラ')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
