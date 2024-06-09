#!/usr/bin/env python
# coding: utf-8
import PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

import sys
import pandas as pd
# Reference
# https://qiita.com/hiroyuki_kageyama/items/cb87a0bee98c0262a35e
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class SPCChart(FigureCanvas):
    fig = Figure()

    def __init__(self, df: pd.DataFrame, metrics: dict):
        super().__init__(self.fig)
        self.init_chart(df, metrics)

    def init_chart(self, df, metrics):
        ax = self.fig.add_subplot(111)
        # chart title
        ax.set(title=metrics['title'])
        ax.set_xlabel(metrics['x'])
        ax.set_ylabel(metrics['y'])
        ax.grid(True)
        # _____________________________________________________________________
        # Horizontal Lines for SPC metrics
        ax.axhline(y=metrics['usl'], linewidth=1, color='red', label='USL')
        ax.axhline(y=metrics['target'], linewidth=1, color='blue', label='Target')
        ax.axhline(y=metrics['lsl'], linewidth=1, color='red', label='LSL')
        ax.axhline(y=metrics['mean'], linewidth=1, color='green', label='Avg')
        # _____________________________________________________________________
        # Trend
        ax.plot(df[metrics['x']], df[metrics['y']], color='gray', marker='o', markersize=10)
        ax.yaxis.label.set_color('gray')
        ax.tick_params(axis='y', colors='gray')
        # add extra ticks
        extraticks = [metrics['lsl'], metrics['target'], metrics['usl']]
        ax.set_yticks(list(ax.get_yticks()) + extraticks)
        self.fig.canvas.draw()
        # _____________________________________________________________________
        # Labels
        labels = [item.get_text() for item in ax.get_yticklabels()]
        n = len(labels)
        labels[n - 3] = 'LSL = ' + str(metrics['lsl'])
        labels[n - 2] = 'Target = ' + str(metrics['target'])
        labels[n - 1] = 'USL = ' + str(metrics['usl'])
        ax.set_yticklabels(labels)
        # Color
        yticklabels = ax.get_yticklabels()
        n = len(yticklabels)
        yticklabels[n - 3].set_color('red')
        yticklabels[n - 2].set_color('blue')
        yticklabels[n - 1].set_color('red')
        # _____________________________________________________________________
        # add second y axis with same range as first y axis
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.tick_params(axis='y', colors='gray')
        # add extra ticks
        extraticks2 = [metrics['mean']]
        ax2.set_yticks(list(ax2.get_yticks()) + extraticks2)
        # Label for second y axis
        labels2 = [item.get_text() for item in ax2.get_yticklabels()]
        n = len(labels2)
        labels2[n - 1] = 'Avg = ' + str(metrics['mean'])
        ax2.set_yticklabels(labels2)
        # Color for second y axis
        yticklabels2 = ax2.get_yticklabels()
        n = len(yticklabels2)
        yticklabels2[n - 1].set_color('green')


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SPC Chart Example')
        self.init_ui()
        self.resize(1000, 500)
        print('PySide6', PySide6.__version__)
        print('matplotlib', matplotlib.__version__)

    def init_ui(self):
        # Example dataframe
        df = pd.DataFrame({
            'Sample': list(range(1, 11)),
            'Y': [9.030, 8.810, 9.402, 8.664, 8.773, 8.774, 8.416, 9.101, 8.687, 8.767]
        })
        # SPC metrics
        metrics = {}
        metrics['title'] = 'Sample SPC chart'
        metrics['x'] = 'Sample'
        metrics['y'] = 'Y'
        metrics['usl'] = 9.97
        metrics['target'] = 8.70
        metrics['lsl'] = 7.43
        metrics['mean'] = df.describe().at['mean', 'Y']
        # _____________________________________________________________________
        # Canvas
        canvas = SPCChart(df, metrics)
        self.setCentralWidget(canvas)
        # _____________________________________________________________________
        # Navigation Toolbar
        toolbar = NavigationToolbar(canvas, self)
        unwanted_buttons = ['Back', 'Forward']
        for x in toolbar.actions():
            if x.text() in unwanted_buttons:
                toolbar.removeAction(x)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
