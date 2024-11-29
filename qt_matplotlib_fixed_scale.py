import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class MyChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.setFixedSize(1200, 600)

        # font setting
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = ax = self.fig.add_subplot(111)
        ax.set_ylabel('Price')
        ax.grid(which='major', linestyle='-', linewidth=0.75, color='gray')
        ax.minorticks_on()
        ax.yaxis.set_major_locator(MultipleLocator(50))
        ax.yaxis.set_minor_locator(MultipleLocator(10))
        ax.grid(which='minor', linestyle='dotted', linewidth=0.75, color='gray')
        ax.grid(True, which='both')

        self.fig.subplots_adjust(
            top=0.98,
            bottom=0.04,
            left=0.09,
            right=0.95,
        )


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart = chart = MyChart()
        self.setCentralWidget(chart)

        toolbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)

        file_pickle = 'pickle/8035_2024-11-13.pkl'
        df = pd.read_pickle(file_pickle)
        self.draw(df)

    def draw(self, df):
        self.chart.ax.plot(df)
        price0 = df['Price'].median()
        delta = 150
        self.chart.ax.set_ylim(price0 - delta, price0 + delta)
        #self.chart.ax.set_ylim(None, None)
        print(self.chart.ax.get_ylim())
def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
