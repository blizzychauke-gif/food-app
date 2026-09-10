from app.config import settings
from app.providers.notifications.mock import MockNotificationProvider
from app.providers.notifications.firebase import FirebaseNotificationProvider
def get_notification_provider():
    if settings.NOTIFICATION_PROVIDER=="firebase": return FirebaseNotificationProvider()
    return MockNotificationProvider()