import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QStyle,
    QToolBar,
)

from load_plugins import load_plugins
from plugins.abstract import PluginTemplate


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        # プラグインの一覧を取得
        plugins: dict[str, type] = load_plugins(
            path_plugin="./plugins",
            package_name="plugins",
            plugin_base_class=PluginTemplate
        )

        self.setWindowTitle("Plugin Sample")

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.combo = combo = QComboBox()
        for key in sorted(plugins.keys()):
            cls = plugins[key]
            combo.addItem(key, cls)
        toolbar.addWidget(combo)

        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay
        )
        action_play = QAction(self)
        action_play.setIcon(icon)
        action_play.triggered.connect(self.on_play)
        toolbar.addAction(action_play)

    def on_play(self):
        cls = self.combo.currentData()
        obj = cls()
        obj.run()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
