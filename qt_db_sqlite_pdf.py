import os
import sys
import tempfile

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QWidget,
)

from qt_db_common_pdf import (
    get_content_from_filename,
    get_list_file,
    insert_filename_content,
)


class SQLitePDF(QMainWindow):
    app_title = 'SQLite & PDF test'

    def __init__(self):
        super().__init__()
        self.con = self.get_connection()
        self.init_table()

        self.combo = None
        self.init_ui()

        self.setWindowTitle(self.app_title)
        self.resize(600, 800)

        self.update_filelist()

    @staticmethod
    def create_table():
        query = QSqlQuery()
        sql = """
            CREATE TABLE IF NOT EXISTS pdfrepo (
                name_file TEXT UNIQUE,
                content NONE
            );
        """
        if not query.exec(sql):
            print(query.lastError())

    @staticmethod
    def get_connection() -> QSqlDatabase:
        con = QSqlDatabase.addDatabase('QSQLITE')
        dbname = 'testdb.sqlite'
        con.setDatabaseName(dbname)
        return con

    def init_table(self):
        if self.con.open():
            self.create_table()
            self.con.close()

    def init_ui(self):
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')

        file_open = QAction('Open', self)
        file_open.setShortcut('Ctrl+O')
        file_open.setStatusTip('open PDF file')
        file_open.triggered.connect(self.show_dialog)
        menu_file.addAction(file_open)

        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.combo = combo = QComboBox()
        combo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        combo.currentTextChanged.connect(self.on_current_text_changed)
        toolbar.addWidget(combo)

        view = QPdfView(self)
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.setCentralWidget(view)

    def show_dialog(self):
        dialog = QFileDialog()
        dialog.setWindowTitle('PDF file selection')
        dialog.setNameFilters(['PDF files (*.pdf)'])
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            basename = os.path.basename(filename)
            f = open(filename, 'rb')
            with f:
                content = f.read()

            if self.con.open():
                insert_filename_content(basename, content)
                self.con.close()
                self.update_filelist()
                self.combo.setCurrentText(basename)

    def update_filelist(self):
        list_name_file = list()
        if self.con.open():
            get_list_file(list_name_file)
            self.con.close()

        self.combo.clear()
        for name_file in list_name_file:
            self.combo.addItem(name_file)

    def on_current_text_changed(self):
        filename = self.combo.currentText()
        if len(filename) == 0:
            return

        if self.con.open():
            content = get_content_from_filename(filename)
            self.con.close()

            if content is not None:
                filepath = os.path.join(tempfile.gettempdir(), filename)
                with open(filepath, 'wb') as f:
                    f.write(content)
                document = QPdfDocument(self)
                document.load(filepath)
                view: QWidget | QPdfView = self.centralWidget()
                view.setDocument(document)


def main():
    app = QApplication()
    ex = SQLitePDF()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
