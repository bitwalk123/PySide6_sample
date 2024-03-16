import sys

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QMainWindow,
)

from qt_mainwindow_dockwidget import MyDockWidget
from qt_mainwindow_menubar import MyMenuBar
from qt_mainwindow_statusbar import MyStatusBar
from qt_mainwindow_toolbar import MyToolBar


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QMainWindow')

        menubar = MyMenuBar()
        menubar.openTriggered.connect(self.on_open)
        menubar.exitTriggered.connect(self.on_exit)
        self.setMenuBar(menubar)

        self.toolbar = toolbar = MyToolBar()
        toolbar.openClicked.connect(self.on_open)
        self.addToolBar(toolbar)

        statusbar = MyStatusBar()
        self.setStatusBar(statusbar)

        dock_top = MyDockWidget('Top', 'topbottom')
        self.addDockWidget(
            Qt.DockWidgetArea.TopDockWidgetArea,
            dock_top
        )

        dock_left = MyDockWidget('Left', 'leftright')
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            dock_left
        )

        dock_right = MyDockWidget('Right', 'leftright')
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock_right
        )

        dock_bottom = MyDockWidget('Bottom', 'topbottom')
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )

        base = QLabel('Central Widget')
        base.setAlignment(Qt.AlignmentFlag.AlignCenter)
        base.setMinimumSize(300, 200)
        base.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        base.setLineWidth(1)
        self.setCentralWidget(base)

    def closeEvent(self, event):
        print('アプリケーションを終了します。')
        event.accept()  # let the window close

    def on_open(self):
        print('Open は未実装です')

    def on_exit(self):
        QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
