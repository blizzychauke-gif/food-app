from app.providers.email.interface import EmailProvider
class ResendEmailProvider(EmailProvider):
    def send_email(self, to, subject, html): raise NotImplementedError("Set RESEND_API_KEY")