from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def run(self, **kwargs):
        pass

    @abstractmethod
    def name(self) -> str:
        pass
