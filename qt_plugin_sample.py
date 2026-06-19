import importlib
import inspect
import pkgutil
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QStyle,
    QToolBar,
)

from plugins.abstract import PluginTemplate


def load_plugins(
        path_plugin: str,
        package_name: str,
        plugin_base_class: type
) -> dict[str, type]:
    # NOTE:
    # 現在はプロジェクト配下のパッケージのみを対象としているため、
    # importlib.import_module() を利用している。
    #
    # 将来的にユーザーが任意のディレクトリへ配置した外部プラグインを
    # 読み込む場合は、sys.path の追加、または
    # importlib.util.spec_from_file_location() を利用した
    # ファイルパスベースのロード方式を検討すること。
    dict_plugin = {}
    for _, module_name, _ in pkgutil.iter_modules([path_plugin]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, plugin_base_class) and cls is not plugin_base_class:
                dict_plugin[cls.NAME] = cls
    return dict_plugin


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
