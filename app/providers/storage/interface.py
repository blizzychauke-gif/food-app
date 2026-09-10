from abc import ABC, abstractmethod
class StorageProvider(ABC):
    @abstractmethod
    def upload(self, filename: str, seed: str="food") -> str: ...