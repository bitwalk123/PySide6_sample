import base64
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


class Example(QMainWindow):
    dbname = 'test.sqlite'
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(dbname)

    def __init__(self):
        super().__init__()
        self.combo = None
        if not os.path.exists(self.dbname):
            self.init_db()

        self.init_ui()
        self.update_filelist()
        self.setWindowTitle('SQLite PDF Test')
        self.resize(600, 800)

    def init_ui(self):
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')

        file_open = QAction('Open', self)
        file_open.setShortcut('Ctrl+O')
        file_open.setStatusTip('Open New File')
        file_open.triggered.connect(self.show_dlg)
        menu_file.addAction(file_open)

        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.combo = QComboBox()
        self.combo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        self.combo.currentTextChanged.connect(self.on_click_open)
        toolbar.addWidget(self.combo)

        view = QPdfView(self)
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.setCentralWidget(view)

    def show_dlg(self):
        dialog = QFileDialog()
        dialog.setNameFilters(['PDF files (*.pdf)'])
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            name_file = os.path.basename(filename)
            f = open(filename, 'rb')
            with f:
                content = base64.b64encode(f.read())
                print(type(content))
                content_str: str = content.decode()

            if self.con.open():
                sql = 'INSERT INTO file VALUES(?, ?);'
                query = QSqlQuery()
                query.prepare(sql)
                query.bindValue(0, name_file)
                # query.bindValue(1, content, type=QSql.ParamTypeFlag.In | QSql.ParamTypeFlag.Binary)
                query.bindValue(1, content_str)
                if not query.exec():
                    print(query.lastError())
                self.con.close()
                self.update_filelist()
                self.combo.setCurrentText(name_file)

    def update_filelist(self):
        list_name_file = list()
        if self.con.open():
            query = QSqlQuery()
            sql = 'SELECT name_file FROM file;'
            query.exec(sql)
            while query.next():
                list_name_file.append(query.value(0))
            self.con.close()

        self.combo.clear()
        # self.combo.clearEditText()
        for name_file in list_name_file:
            self.combo.addItem(name_file)

    def on_click_open(self):
        filename = self.combo.currentText()
        if len(filename) == 0:
            return

        if self.con.open():
            content = None
            query = QSqlQuery()
            sql = 'SELECT content FROM file WHERE name_file = "%s";' % filename
            query.exec(sql)
            if query.next():
                content_str = query.value(0)
                content = base64.b64decode(content_str.encode())
            self.con.close()

            if content is not None:
                filepath = os.path.join(tempfile.gettempdir(), filename)
                with open(filepath, 'wb') as f:
                    f.write(content)
                document = QPdfDocument(self)
                document.load(filepath)
                view: QWidget | QPdfView = self.centralWidget()
                view.setDocument(document)

    def init_db(self):
        if self.con.open():
            query = QSqlQuery()
            sql = 'CREATE TABLE file (name_file TEXT UNIQUE, content NONE);'
            query.exec(sql)
            self.con.close()


def main():
    app = QApplication()
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
