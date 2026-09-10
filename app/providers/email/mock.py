from app.providers.email.interface import EmailProvider
EMAIL_OUTBOX=[]
class MockEmailProvider(EmailProvider):
    def send_email(self, to, subject, html):
        m={"to":to,"subject":subject,"html":html}
        EMAIL_OUTBOX.append(m); print(f"[MOCK EMAIL] to={to} subj={subject}")
        return {"logged": True}