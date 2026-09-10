import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    OTP_PROVIDER: str = os.getenv("OTP_PROVIDER", "mock").lower()
    PAYMENT_PROVIDER: str = os.getenv("PAYMENT_PROVIDER", "mock").lower()
    MAP_PROVIDER: str = os.getenv("MAP_PROVIDER", "mock").lower()
    NOTIFICATION_PROVIDER: str = os.getenv("NOTIFICATION_PROVIDER", "mock").lower()
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "mock").lower()
    EMAIL_PROVIDER: str = os.getenv("EMAIL_PROVIDER", "mock").lower()
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fooddash.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    PAYFAST_MODE: str = os.getenv("PAYFAST_MODE", "sandbox")
    PAYFAST_RETURN_URL: str = os.getenv("PAYFAST_RETURN_URL", "http://localhost:8000/payment/success")
    PAYFAST_CANCEL_URL: str = os.getenv("PAYFAST_CANCEL_URL", "http://localhost:8000/payment/cancel")
    PAYFAST_NOTIFY_URL: str = os.getenv("PAYFAST_NOTIFY_URL", "http://localhost:8000/api/payments/payfast/itn")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    PAYFAST_MERCHANT_ID: str = os.getenv("PAYFAST_MERCHANT_ID", "")
    PAYFAST_MERCHANT_KEY: str = os.getenv("PAYFAST_MERCHANT_KEY", "")
    PAYFAST_PASSPHRASE: str = os.getenv("PAYFAST_PASSPHRASE", "")

    @property
    def IS_DEV(self) -> bool:
        return self.APP_ENV != "production"

settings = Settings()

def provider_status():
    return {
        "OTP": settings.OTP_PROVIDER.upper(),
        "Payments": settings.PAYMENT_PROVIDER.upper(),
        "Maps": settings.MAP_PROVIDER.upper(),
        "Notifications": settings.NOTIFICATION_PROVIDER.upper(),
        "Storage": settings.STORAGE_PROVIDER.upper(),
        "Email": settings.EMAIL_PROVIDER.upper(),
        "mode": settings.APP_ENV
    }