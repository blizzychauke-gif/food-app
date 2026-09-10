from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.deps import get_payments, get_maps, get_notifs, get_email
from app.services.order_service import OrderService
router=APIRouter(prefix="/api/payments",tags=["payments"])
class CreateReq(BaseModel): order_id: str
class WebhookReq(BaseModel): payment_id: str; status: str
def svc(): return OrderService(get_payments(),get_maps(),get_notifs(),get_email())
@router.post("/create")
def create(r: CreateReq):
    from app.store import get_by_id
    o=get_by_id("orders",r.order_id)
    if not o: raise HTTPException(404,"order not found")
    pi=get_payments().create_payment(o["id"],o["total"]); o["payment_id"]=pi.id
    return {"id":pi.id,"amount":pi.amount,"status":pi.status,"checkout_url":pi.checkout_url}
@router.get("/{pid}/verify")
def verify(pid: str): return get_payments().verify_payment(pid).__dict__
@router.post("/webhook")
def webhook(r: WebhookReq):
    try: pi=get_payments().handle_webhook({"payment_id":r.payment_id,"status":r.status})
    except Exception as e: raise HTTPException(400,str(e))
    if pi.status.value=="success": return svc().on_payment_success(pi.id)
    if pi.status.value=="failed": return svc().on_payment_failed(pi.id)
    return {"payment":pi.__dict__}
@router.post("/{pid}/refund")
def refund(pid: str):
    pi=get_payments().refund(pid); return pi.__dict__