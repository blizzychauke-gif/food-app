from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from app.deps import get_payments
router=APIRouter(prefix='/api/payments/payfast',tags=['PayFast'])
@router.get('/checkout/{payment_id}',response_class=HTMLResponse)
def checkout(payment_id:str, request:Request):
    from app.providers.payments.payfast import _PAYMENTS
    p=_PAYMENTS.get(payment_id)
    if not p: raise HTTPException(404,'Payment not found')
    action='https://sandbox.payfast.co.za/eng/process' if __import__('app.config',fromlist=['settings']).settings.PAYFAST_MODE!='live' else 'https://www.payfast.co.za/eng/process'
    fields=''.join(f'<input type="hidden" name="{k}" value="{str(v)}">' for k,v in p.items() if k not in ('order_id','amount'))
    return f'<html><body><p>Redirecting to secure PayFast…</p><form id="f" method="post" action="{action}">{fields}</form><script>document.getElementById("f").submit()</script></body></html>'
@router.post('/itn')
async def itn(request:Request):
    payload=dict(await request.form())
    result=get_payments().handle_webhook(payload)
    try:
        from app.store import find_orders_by_payment
        o=find_orders_by_payment(result.id)
        if o: o['status']='PAID' if result.status.value=='success' else 'PAYMENT_FAILED'
    except Exception: pass
    return {'received':True,'payment_id':result.id,'status':result.status.value}
