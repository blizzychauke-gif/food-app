from app.providers.notifications.interface import NotificationProvider
NOTIFICATION_LOG=[]
class MockNotificationProvider(NotificationProvider):
    def send(self, user_id, title, body, role="customer"):
        n={"to":user_id,"title":title,"body":body,"role":role}
        NOTIFICATION_LOG.append(n)
        try:
            from app.store import DB
            DB["notifications"].append(n)
        except: pass
        print(f"[MOCK PUSH:{role}] {user_id} | {title} - {body}")
        return {"sent": True, **n}