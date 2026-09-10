import uuid
from app.providers.payments.interface import PaymentProvider, PaymentIntent, PaymentStatus
_store = {}
class MockPaymentProvider(PaymentProvider):
    def create_payment(self, order_id, amount, currency="ZAR"):
        pid = f"mock_{uuid.uuid4().hex[:8]}"
        pi = PaymentIntent(id=pid, order_id=order_id, amount=amount, currency=currency, checkout_url=f"/dev/mock-pay/{pid}")
        _store[pid]=pi
        print(f"[MOCK PAY] initiated {pid} R{amount} for {order_id}")
        return pi
    def verify_payment(self, payment_id):
        if payment_id not in _store: raise ValueError("payment not found")
        return _store[payment_id]
    def refund(self, payment_id):
        pi=self.verify_payment(payment_id); pi.status=PaymentStatus.REFUNDED; return pi
    def handle_webhook(self, payload: dict):
        pid=payload["payment_id"]; pi=self.verify_payment(pid)
        pi.status=PaymentStatus(payload["status"]); return pi
    def simulate_success(self, pid): pi=self.verify_payment(pid); pi.status=PaymentStatus.SUCCESS; return pi
    def simulate_failed(self, pid): pi=self.verify_payment(pid); pi.status=PaymentStatus.FAILED; return pi
    def simulate_cancelled(self, pid): pi=self.verify_payment(pid); pi.status=PaymentStatus.CANCELLED; return pi