from plugins.abstract import PluginTemplate


class Plugin(PluginTemplate):
    NAME = "simple 2"

    def run(self) -> None:
        print(self.NAME)
