from app.config import settings
from app.providers.email.mock import MockEmailProvider
from app.providers.email.resend import ResendEmailProvider
def get_email_provider():
    if settings.EMAIL_PROVIDER=="resend": return ResendEmailProvider()
    return MockEmailProvider()