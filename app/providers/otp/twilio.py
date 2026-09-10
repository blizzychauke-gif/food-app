from app.providers.otp.interface import OTPProvider
class TwilioOTPProvider(OTPProvider):
    """REAL placeholder. Implement with Twilio Verify API. See docs/REAL_API_MIGRATION.md"""
    def __init__(self, sid=None, token=None, service_sid=None):
        self.sid=sid; self.token=token; self.service_sid=service_sid
    def send_otp(self, phone: str):
        raise NotImplementedError("Configure TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN / TWILIO_VERIFY_SID and implement Verify create.")
    def verify_otp(self, phone: str, code: str):
        raise NotImplementedError("Configure Twilio and implement Verify check.")
    def resend_otp(self, phone: str):
        raise NotImplementedError("Configure Twilio.")