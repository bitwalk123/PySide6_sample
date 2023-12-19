import sys

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        file_path = 'sample.pdf'
        self.init_ui(file_path)
        self.resize(600, 800)

    def init_ui(self, file_path):
        document = QPdfDocument(self)
        document.load(file_path)
        view = QPdfView(self)
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setZoomMode(QPdfView.ZoomMode.FitInView)
        view.setDocument(document)
        self.setCentralWidget(view)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
