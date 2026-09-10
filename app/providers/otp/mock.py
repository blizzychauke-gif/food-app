import random, logging
from datetime import datetime, timedelta
from app.config import settings
from app.providers.otp.interface import OTPProvider
log = logging.getLogger("mock-otp")
_store = {}
OTP_LOGS = []

class MockOTPProvider(OTPProvider):
    EXPIRY = 300
    MAX_ATTEMPTS = 5
    def send_otp(self, phone: str):
        code = f"{random.randint(100000,999999)}"
        _store[phone] = {"code": code, "expires": datetime.utcnow()+timedelta(seconds=self.EXPIRY), "attempts": 0}
        log.warning(f"[MOCK OTP] {phone} -> {code}")
        print(f"[MOCK OTP] {phone} -> {code}")
        OTP_LOGS.append({"phone": phone, "code": code, "time": str(datetime.utcnow())})
        res = {"sent": True, "expires_in": self.EXPIRY}
        if settings.IS_DEV:
            res["dev_code"] = code
        return res
    def verify_otp(self, phone: str, code: str):
        r = _store.get(phone)
        if not r:
            raise ValueError("No OTP requested. Call send first.")
        if datetime.utcnow() > r["expires"]:
            del _store[phone]
            raise ValueError("OTP expired")
        r["attempts"] += 1
        if r["attempts"] > self.MAX_ATTEMPTS:
            del _store[phone]
            raise ValueError("Too many attempts")
        if r["code"] != code:
            return False
        del _store[phone]
        return True
    def resend_otp(self, phone: str):
        return self.send_otp(phone)