from fastapi import APIRouter, HTTPException
from app.config import settings, provider_status
from app.deps import get_payments, get_maps, get_notifs, get_email
from app.services.order_service import OrderService
from app.providers.maps.interface import Coords
router=APIRouter(prefix="/api/dev",tags=["dev"])
def guard():
    if not settings.IS_DEV: raise HTTPException(404)
def svc(): return OrderService(get_payments(),get_maps(),get_notifs(),get_email())
@router.get("/providers")
def prov(): guard(); return provider_status()
@router.get("/otp-logs")
def otp_logs(): guard(); from app.providers.otp.mock import OTP_LOGS; return OTP_LOGS[-20:]
@router.get("/emails")
def emails(): guard(); from app.providers.email.mock import EMAIL_OUTBOX; return EMAIL_OUTBOX[-20:]
@router.get("/notifications")
def notifs(): guard(); from app.providers.notifications.mock import NOTIFICATION_LOG; return NOTIFICATION_LOG[-30:]
@router.post("/simulate/payment-success")
def pay_ok(payment_id: str):
    guard()
    try: get_payments().simulate_success(payment_id)
    except AttributeError: raise HTTPException(400,"Only mock provider supports simulation")
    except Exception as e: raise HTTPException(400,str(e))
    return svc().on_payment_success(payment_id)
@router.post("/simulate/payment-failed")
def pay_fail(payment_id: str):
    guard()
    get_payments().simulate_failed(payment_id)
    return svc().on_payment_failed(payment_id)
@router.post("/simulate/restaurant-accept")
def accept(order_id: str): guard(); return svc().update_status(order_id,"ACCEPTED")
@router.post("/simulate/preparation")
def prep(order_id: str): guard(); return svc().update_status(order_id,"PREPARING")
@router.post("/simulate/delivery")
async def delivery(order_id: str):
    guard()
    from app.store import get_by_id
    from app.tracking.simulator import simulate_driver
    from app.tracking.manager import manager
    o=svc().update_status(order_id,"ON_THE_WAY")
    route=get_maps().route(Coords(o["restaurant_lat"],o["restaurant_lng"]),Coords(o["customer_lat"],o["customer_lng"]))
    await simulate_driver(order_id,route.polyline)
    await manager.broadcast(order_id,{"type":"status","order_id":order_id,"status":"ON_THE_WAY","distance_km":route.distance_km,"eta_min":route.eta_min})
    return {"order":o,"route":{"distance_km":route.distance_km,"eta_min":route.eta_min}}
@router.post("/simulate/driver-movement")
async def move(order_id: str):
    guard()
    from app.store import get_by_id
    from app.tracking.simulator import simulate_driver
    o=get_by_id("orders",order_id)
    if not o: raise HTTPException(404,"order not found")
    route=get_maps().route(Coords(o["restaurant_lat"],o["restaurant_lng"]),Coords(o["customer_lat"],o["customer_lng"]))
    return await simulate_driver(order_id,route.polyline)
@router.post("/simulate/test-notification")
def test_notif(user_id: str="u1", role: str="customer"):
    guard(); return get_notifs().send(user_id,"Test push","Hello from DEV dashboard",role=role)