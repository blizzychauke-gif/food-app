from app.config import settings
from app.providers.payments.mock import MockPaymentProvider
from app.providers.payments.payfast import PayFastPaymentProvider
def get_payment_provider():
    if settings.PAYMENT_PROVIDER=="payfast": return PayFastPaymentProvider()
    return MockPaymentProvider()