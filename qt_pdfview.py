import os
import sys

from PySide6.QtCore import QPointF, QEvent
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
        self.resize(800, 900)
        self.setWindowTitle("PDFViewer")

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Open
        icon_open = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        self.action_open = action_open = QAction(icon_open, "Open PDF file", self)
        action_open.triggered.connect(self.on_select_pdf)
        toolbar.addAction(action_open)

        toolbar.addSeparator()

        # Prev
        icon_prev = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        self.action_prev = action_prev = QAction(icon_prev, "Previous Page", self)
        action_prev.triggered.connect(self.on_page_prev)
        action_prev.setShortcut("Left")
        toolbar.addAction(action_prev)

        # Next
        icon_next = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        self.action_next = action_next = QAction(icon_next, "Next Page", self)
        action_next.triggered.connect(self.on_page_next)
        action_next.setShortcut("Right")
        toolbar.addAction(action_next)

        toolbar.addSeparator()

        # Zoom Out
        icon_zoom_out = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)
        self.action_zoom_out = action_zoom_out = QAction(icon_zoom_out, "Zoom Out", self)
        action_zoom_out.triggered.connect(self.on_zoom_out)
        toolbar.addAction(action_zoom_out)

        # Fit In View
        icon_fit = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.action_fit = action_fit = QAction(icon_fit, "Fit In View", self)
        action_fit.triggered.connect(self.on_fit_in_view)
        toolbar.addAction(action_fit)

        # Zoom In
        icon_zoom_in = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        self.action_zoom_in = action_zoom_in = QAction(icon_zoom_in, "Zoom In", self)
        action_zoom_in.triggered.connect(self.on_zoom_in)
        toolbar.addAction(action_zoom_in)

        toolbar.addSeparator()

        # PDF View
        self.view = view = QPdfView(self)
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setZoomMode(QPdfView.ZoomMode.FitInView)
        view.installEventFilter(self)  # マウスホイールでページ移動
        self.setCentralWidget(view)

        # Status bar
        self.status = self.statusBar()

        # 初期状態ではページ移動不可
        self.update_nav_buttons()

    def eventFilter(self, obj, event: QEvent):
        """
        マウスホイールでページ移動
        """
        if self.doc is None:
            return False

        if obj is self.view and event.type() == QEvent.Type.Wheel:
            delta = event.angleDelta().y()
            nav = self.view.pageNavigator()

            if delta < 0:
                nav.jump(nav.currentPage() + 1, QPointF(0, 0))
            else:
                nav.jump(nav.currentPage() - 1, QPointF(0, 0))

            self.update_page_status()
            self.update_nav_buttons()
            return True

        return super().eventFilter(obj, event)

    def on_fit_in_view(self):
        """
        画面にフィット
        """
        self.view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.view.setZoomFactor(1.0)  # ★ 内部 zoomFactor をリセット

    def on_select_pdf(self):
        """
        PDF を開く
        """
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

        self.update_page_status()
        self.update_nav_buttons()

    def on_page_next(self):
        """
        ページ移動（次へ）
        """
        self.set_page_step(1)

    def on_page_prev(self):
        """
        ページ移動（前へ）
        """
        self.set_page_step(-1)

    def on_zoom_in(self):
        """
        ズームイン
        """
        self.set_zoom_factor(1.1)

    def on_zoom_out(self):
        """
        ズームアウト
        """
        self.set_zoom_factor(0.9)

    def set_page_step(self, step: int):
        """
        指定ステップ分のページ移動
        """
        if self.doc is None:
            return
        nav = self.view.pageNavigator()
        nav.jump(nav.currentPage() + step, QPointF(0, 0))
        self.update_page_status()
        self.update_nav_buttons()

    def set_zoom_factor(self, factor: float):
        """
        指定ファクタ分のズーム
        """
        self.view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.view.setZoomFactor(self.view.zoomFactor() * factor)

    def update_nav_buttons(self):
        """
        ページ移動ボタンの enable/disable
        """
        if self.doc is None:
            self.action_prev.setEnabled(False)
            self.action_next.setEnabled(False)
            return

        nav = self.view.pageNavigator()
        page = nav.currentPage()
        total = self.doc.pageCount()

        self.action_prev.setEnabled(0 < page)
        self.action_next.setEnabled(page < total - 1)

    def update_page_status(self):
        """
        ステータスバー更新
        """
        if self.doc is None:
            self.status.showMessage("")
            return
        nav = self.view.pageNavigator()
        page = nav.currentPage()
        total = self.doc.pageCount()
        self.status.showMessage(f"Page {page + 1} / {total}")


def main():
    app = QApplication(sys.argv)
    win = PDFViewer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
