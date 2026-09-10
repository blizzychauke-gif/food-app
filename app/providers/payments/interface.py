from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
class PaymentStatus(str, Enum):
    INITIATED="initiated"; SUCCESS="success"; FAILED="failed"; CANCELLED="cancelled"; REFUNDED="refunded"
@dataclass
class PaymentIntent:
    id: str; order_id: str; amount: float; currency: str="ZAR"; status: PaymentStatus=PaymentStatus.INITIATED; checkout_url: str=""
class PaymentProvider(ABC):
    @abstractmethod
    def create_payment(self, order_id: str, amount: float, currency="ZAR") -> PaymentIntent: ...
    @abstractmethod
    def verify_payment(self, payment_id: str) -> PaymentIntent: ...
    @abstractmethod
    def refund(self, payment_id: str) -> PaymentIntent: ...
    @abstractmethod
    def handle_webhook(self, payload: dict) -> PaymentIntent: ...