from abc import ABC, abstractmethod


class PluginTemplate(ABC):
    NAME = "template"

    @abstractmethod
    def run(self) -> None: ...
