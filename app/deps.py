from app.providers.otp.factory import get_otp_provider as _otp
from app.providers.payments.factory import get_payment_provider as _pay
from app.providers.maps.factory import get_maps_provider as _maps
from app.providers.notifications.factory import get_notification_provider as _notif
from app.providers.storage.factory import get_storage_provider as _stor
from app.providers.email.factory import get_email_provider as _email

_cache={}
def get_otp():
    if "otp" not in _cache: _cache["otp"]=_otp()
    return _cache["otp"]
def get_payments():
    if "pay" not in _cache: _cache["pay"]=_pay()
    return _cache["pay"]
def get_maps():
    if "maps" not in _cache: _cache["maps"]=_maps()
    return _cache["maps"]
def get_notifs():
    if "notif" not in _cache: _cache["notif"]=_notif()
    return _cache["notif"]
def get_storage():
    if "stor" not in _cache: _cache["stor"]=_stor()
    return _cache["stor"]
def get_email():
    if "email" not in _cache: _cache["email"]=_email()
    return _cache["email"]