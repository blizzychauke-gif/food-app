import hashlib, urllib.parse, uuid
import requests
from app.config import settings
from app.providers.payments.interface import PaymentProvider, PaymentIntent, PaymentStatus

class PayFastPaymentProvider(PaymentProvider):
    def __init__(self): self.mode=settings.PAYFAST_MODE; self.base='https://sandbox.payfast.co.za' if self.mode!='live' else 'https://www.payfast.co.za'
    def _signature(self,data):
        pairs=[]
        for k,v in data.items():
            if v is None or k=='signature': continue
            pairs.append(f'{k}={urllib.parse.quote_plus(str(v).strip())}')
        query='&'.join(pairs)
        if settings.PAYFAST_PASSPHRASE: query += '&passphrase='+urllib.parse.quote_plus(settings.PAYFAST_PASSPHRASE.strip())
        return hashlib.md5(query.encode()).hexdigest()
    def create_payment(self,order_id,amount,currency='ZAR'):
        if not settings.PAYFAST_MERCHANT_ID or not settings.PAYFAST_MERCHANT_KEY: raise ValueError('Configure PayFast credentials')
        pid=f'pf_{uuid.uuid4().hex[:12]}'
        data={'merchant_id':settings.PAYFAST_MERCHANT_ID,'merchant_key':settings.PAYFAST_MERCHANT_KEY,'amount':f'{amount:.2f}','item_name':f'FoodDash order {order_id}','m_payment_id':pid,'return_url':settings.PAYFAST_RETURN_URL,'cancel_url':settings.PAYFAST_CANCEL_URL,'notify_url':settings.PAYFAST_NOTIFY_URL}
        data['signature']=self._signature(data)
        checkout=f"{settings.PUBLIC_BASE_URL}/api/payments/payfast/checkout/{pid}?"+urllib.parse.urlencode(data)
        _PAYMENTS[pid]=data|{'order_id':order_id,'amount':amount}
        return PaymentIntent(pid,order_id,amount,currency,PaymentStatus.INITIATED,checkout)
    def verify_payment(self,payment_id):
        x=_PAYMENTS.get(payment_id)
        if not x: raise ValueError('payment not found')
        return PaymentIntent(payment_id,x['order_id'],float(x['amount']),status=PaymentStatus.INITIATED,checkout_url='')
    def refund(self,payment_id): raise NotImplementedError('PayFast refunds should be handled through your merchant process')
    def handle_webhook(self,payload):
        pid=payload.get('m_payment_id') or payload.get('payment_id'); x=_PAYMENTS.get(pid)
        if not x: raise ValueError('Unknown payment')
        status=PaymentStatus.SUCCESS if payload.get('payment_status')=='COMPLETE' else PaymentStatus.FAILED
        return PaymentIntent(pid,x['order_id'],float(x['amount']),status=status,checkout_url='')
_PAYMENTS={}
