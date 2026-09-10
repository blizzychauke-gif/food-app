from app.providers.notifications.interface import NotificationProvider
class FirebaseNotificationProvider(NotificationProvider):
    def send(self, user_id, title, body, role="customer"): raise NotImplementedError("Set FIREBASE_CREDENTIALS_JSON")