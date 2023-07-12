import random
import sys
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QToolButton,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class MyCanvas(FigureCanvas):

    def __init__(self):
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)

        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 16

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def clearAxes(self):
        self.axes.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()


class Example(QMainWindow):
    count = 1

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Ploy Example')

    def init_ui(self):
        id = QFontDatabase.addApplicationFont(FONT_PATH)
        if id < 0:
            print("Error")
            sys.exit()
        families = QFontDatabase.applicationFontFamilies(id)
        print(families)
        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbutton = QToolButton()
        toolbutton.setText('更新')
        toolbutton.setFont(QFont(families[0], 12))
        toolbutton.clicked.connect(self.toolButtonClicked)
        toolbar.addWidget(toolbutton)
        self.plot = MyCanvas()
        self.draw_plot()
        self.setCentralWidget(self.plot)

    def toolButtonClicked(self):
        self.plot.clearAxes()
        self.draw_plot()
        self.plot.refreshDraw()

    def draw_plot(self):
        # TEST PLOTS
        n_data = 100
        list_x = [x for x in range(n_data)]
        list_y = [(random.random() - 0.5) * 100 for i in range(n_data)]
        self.plot.axes.plot(list_x, list_y)
        #
        self.plot.axes.set_title('テスト %d' % self.count)
        self.plot.axes.set_xlabel('X軸')
        self.plot.axes.set_ylabel('Y軸')
        self.plot.axes.grid()
        self.count += 1


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
