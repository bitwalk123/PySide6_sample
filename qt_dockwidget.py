# conding: utf-8
# Reference:
# https://dungeonneko.hatenablog.com/entry/2015/07/19/123958
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# entry point
if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    wnd = QMainWindow()

    # Dock Widgets
    wnd.__c = QTextEdit(wnd)
    wnd.__l = QDockWidget("Left", wnd)
    wnd.__r = QDockWidget("Right", wnd)
    wnd.__t = QDockWidget("Top", wnd)
    wnd.__b = QDockWidget("Bottom", wnd)

    wnd.setCentralWidget(wnd.__c)
    wnd.addDockWidget(Qt.LeftDockWidgetArea, wnd.__l)
    wnd.addDockWidget(Qt.RightDockWidgetArea, wnd.__r)
    wnd.addDockWidget(Qt.TopDockWidgetArea, wnd.__t)
    wnd.addDockWidget(Qt.BottomDockWidgetArea, wnd.__b)
    wnd.setWindowTitle('gui example')
    wnd.statusBar()

    # Exit Action
    actionExit = QAction('&Exit', wnd)
    actionExit.setShortcut('Ctrl+Q')
    actionExit.setStatusTip('Quit application')
    actionExit.triggered.connect(wnd.close)
    m = wnd.menuBar().addMenu('&File')
    m.addAction(actionExit)
    t = wnd.addToolBar('Exit')
    t.addAction(actionExit)

    # Window Menu: toggle widget's visibility
    m = wnd.menuBar().addMenu('&Window')
    m.addAction(wnd.__l.toggleViewAction())
    m.addAction(wnd.__r.toggleViewAction())
    m.addAction(wnd.__t.toggleViewAction())
    m.addAction(wnd.__b.toggleViewAction())

    wnd.resize(640, 480)
    wnd.show()
    sys.exit(myapp.exec_())
