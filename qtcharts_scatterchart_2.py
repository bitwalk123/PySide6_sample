import sys
import numpy as np
import pandas as pd
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLegend,
    QScatterSeries, QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class ScatterChart(QChartView):
    def __init__(self, df: pd.DataFrame, target, label_x, label_y):
        super().__init__()
        self.df = df
        self.target = target
        self.label_x = label_x
        self.label_y = label_y

        chart = self.init_ui()
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def init_ui(self):
        chart = QChart()
        # axisX = QValueAxis()
        # axisY = QValueAxis()
        # chart.addAxis(axisX, Qt.AlignBottom)
        # chart.addAxis(axisY, Qt.AlignLeft)

        targets = sorted(list(set(self.df[self.target])))

        for name in targets:
            series = QScatterSeries()
            series.setName(name)
            series.setMarkerShape(QScatterSeries.MarkerShape.MarkerShapeCircle)
            series.setMarkerSize(10.0)

            df2 = self.df[self.df[self.target] == name]
            list_x = df2[self.label_x]
            list_y = df2[self.label_y]
            for x, y in zip(list_x, list_y):
                series.append(x, y)
            # series.attachAxis(axisX)
            # series.attachAxis(axisY)
            chart.addSeries(series)

        # axisX.setRange(-2.8, 3.3)
        # axisY.setRange(-2.7, 2.7)
        chart.setTitle('Simple scatterchart example')
        chart.createDefaultAxes()
        chart.setDropShadowEnabled(False)

        chart.legend().setMarkerShape(QLegend.MarkerShape.MarkerShapeFromSeries)

        return chart


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        df = self.get_pca()
        scatter = ScatterChart(df, 'target', 'PC1', 'PC2')
        self.setCentralWidget(scatter)
        self.resize(500, 500)
        self.setWindowTitle('ScatterChart')

    def get_pca(self) -> pd.DataFrame:
        iris = load_iris()
        features = iris['data']
        iris_dict = {s: iris.target_names[s] for s in range(len(iris.target_names))}

        # Standard Scaler
        pipe_standard = Pipeline(
            steps=[('scaler', StandardScaler()),
                   ('PCA', PCA())]
        )
        components_standard = pipe_standard.fit_transform(features)
        df_pca = pd.DataFrame(
            data=components_standard,
            columns=['PC{}'.format(i + 1) for i in range(components_standard.shape[1])]
        )
        df_pca['target'] = [iris_dict[s] for s in iris.target]

        return df_pca


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
