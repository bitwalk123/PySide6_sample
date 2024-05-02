import sys

from PySide6.QtCore import QTranslator, QLocale, QCoreApplication
from PySide6.QtWidgets import QApplication, QPushButton

if __name__ == "__main__":

    app = QApplication([])
    translator = QTranslator()
    # look up e.g. :/i18n/myapp_de.qm
    if translator.load(QLocale(), "myapp", "_", ":/i18n"):
        QCoreApplication.installTranslator(translator)
    hello = QPushButton(QCoreApplication.translate("main", "Hello world!"))
    hello.resize(100, 30)
    hello.show()
    sys.exit(app.exec())