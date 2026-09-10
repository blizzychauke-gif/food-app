from abc import ABC, abstractmethod
class NotificationProvider(ABC):
    @abstractmethod
    def send(self, user_id: str, title: str, body: str, role: str="customer") -> dict: ...