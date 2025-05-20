# Original was created by Google Gemini
# Modified by Fuhito Suguri
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Matplotlib の Figure と Canvas を作成
        self.figure = Figure()
        self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.grid()
        self.ax.set_title("Real-time Trend Chart")

        # データの初期化
        self.x_data = list()
        self.y_data = list()

        # プロットラインの初期化
        self.line, = self.ax.plot(self.x_data, self.y_data)

        # QTimer の設定 (1秒ごとに update_data メソッドを呼び出す)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 1000ミリ秒 = 1秒

        self.counter = 0

    def update_data(self):
        # 新しいデータを生成 (ここではランダムな値を追加)
        self.counter += 1
        new_x = self.counter
        new_y = random.randint(0, 100)

        # データを追加
        self.x_data.append(new_x)
        self.y_data.append(new_y)

        # グラフを更新
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)

        # x軸の範囲を自動調整 (必要に応じて)
        self.ax.relim()
        self.ax.autoscale_view()

        # Canvas を再描画
        self.canvas.draw()


def main():
    app: QApplication = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
