from plugins.abstract import PluginTemplate


class Plugin(PluginTemplate):
    NAME = "simple 1"

    def run(self) -> None:
        print(self.NAME)
