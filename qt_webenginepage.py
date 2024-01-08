import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
)


class Example(QMainWindow):

    def __init__(self, url: QUrl):
        super().__init__()
        self.init_ui(url)
        self.resize(1000, 800)

    def init_ui(self, url):
        view = QWebEngineView()
        view.load(url)
        view.loadFinished.connect(self.on_load_finished)
        self.setCentralWidget(view)

    def on_load_finished(self, flag: bool) -> bool:
        if not flag:
            return False
        view: QWidget | QWebEngineView = self.centralWidget()
        page: QWebEnginePage = view.page()
        page.runJavaScript(
            'document.documentElement.outerHTML',
            0, self.print_content
        )
        return True

    @staticmethod
    def print_content(content: str):
        print(content)


def main(url: QUrl):
    app = QApplication()
    ex = Example(url)
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    url_init = QUrl('https://www.ueno-panda.jp/')
    main(url_init)
