import os
import sys

from PySide6.QtCore import QPointF
from PySide6.QtGui import QAction
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStyle,
    QToolBar,
)


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.resize(600, 800)
        self.setWindowTitle("PDFViewer")

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        self.action_open = action_open = QAction(icon, "Open PDF file", self)
        action_open.triggered.connect(self.on_select_pdf)
        toolbar.addAction(action_open)

        icon_prev = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        self.action_prev = action_prev = QAction(icon_prev, "Previous Page", self)
        action_prev.triggered.connect(self.on_prev_page)
        toolbar.addAction(action_prev)

        icon_next = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        self.action_next = action_next = QAction(icon_next, "Next Page", self)
        action_next.triggered.connect(self.on_next_page)
        toolbar.addAction(action_next)

        self.view = view = QPdfView(self)
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.setCentralWidget(view)

    def on_select_pdf(self):
        path_pdf, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF Files (*.pdf)"
        )
        if not path_pdf:
            return

        doc = QPdfDocument(self)
        err = doc.load(path_pdf)
        if err != QPdfDocument.Error.None_:
            QMessageBox.warning(self, "Error", f"Failed to load PDF: {err}")
            return

        self.doc = doc
        self.view.setDocument(self.doc)
        self.setWindowTitle(f"PDFViewer - {os.path.basename(path_pdf)}")

    def on_prev_page(self):
        if self.doc is None:
            return
        nav = self.view.pageNavigator()
        nav.jump(nav.currentPage() - 1, QPointF(0, 0))

    def on_next_page(self):
        if self.doc is None:
            return
        nav = self.view.pageNavigator()
        nav.jump(nav.currentPage() + 1, QPointF(0, 0))


def main():
    app = QApplication(sys.argv)
    win = PDFViewer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
