import sys

import numpy as np
import pandas as pd
import seaborn as sns
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle,
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure


class MyNavToolbar(NavigationToolbar):
    def __init__(self, canvas: FigureCanvas):
        super().__init__(canvas)
        user_action = QAction("User", self)
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMenuButton
        )
        user_action.setIcon(icon)
        user_action.triggered.connect(self.on_user_action)

        actions = self.actions()

        n = len(actions)
        self.insertAction(actions[n - 1], user_action)

    def on_user_action(self):
        # Zoomモードなら解除
        if self._actions["zoom"].isChecked():
            self._actions["zoom"].trigger()
        # Panモードなら解除
        if self._actions["pan"].isChecked():
            self._actions["pan"].trigger()

        print("User button clicked")


class Histogram(FigureCanvas):

    def __init__(self, ser: pd.Series):
        fig = Figure()
        super().__init__(fig)
        sns.set_style("whitegrid")
        ax = sns.histplot(data=ser, kde=True, ax=fig.add_subplot(111))
        ax.set(title="Histogram Sample")


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram example")
        self.init_ui()

    def init_ui(self):
        # sample data
        ser = pd.Series(np.random.normal(50, 10, 100), name="Sample")
        # chart
        canvas: FigureCanvas = Histogram(ser)
        self.setCentralWidget(canvas)
        toolbar = MyNavToolbar(canvas)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
