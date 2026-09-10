import os
from app.config import settings
from app.providers.otp.mock import MockOTPProvider
from app.providers.otp.twilio import TwilioOTPProvider
def get_otp_provider():
    if settings.OTP_PROVIDER == "twilio":
        return TwilioOTPProvider(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"), os.getenv("TWILIO_VERIFY_SID"))
    return MockOTPProvider()