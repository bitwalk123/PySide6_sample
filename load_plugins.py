import importlib
import inspect
import pkgutil


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
