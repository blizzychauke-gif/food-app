from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.store import DB, get_by_id
from app.deps import get_payments, get_maps, get_notifs, get_email
from app.services.order_service import OrderService
from app.providers.maps.interface import Coords
from app.tracking.simulator import simulate_driver

router=APIRouter(prefix="/api/orders",tags=["orders"])
def svc(): return OrderService(get_payments(),get_maps(),get_notifs(),get_email())
class Item(BaseModel): food_id: str; qty: int=1
class CheckoutReq(BaseModel):
    customer_id: str; restaurant_id: str; items: List[Item]
    address_id: Optional[str]=None; promo_code: Optional[str]=None
    lat: Optional[float]=None; lng: Optional[float]=None
class StatusReq(BaseModel): status: str

@router.post("/checkout")
async def checkout(r: CheckoutReq):
    try:
        order,pi=svc().checkout(r.customer_id,r.restaurant_id,[i.model_dump() for i in r.items],r.address_id,r.promo_code,r.lat,r.lng)
    except ValueError as e: raise HTTPException(400,str(e))
    return {"order":order,"payment":{"id":pi.id,"amount":pi.amount,"currency":pi.currency,"status":pi.status,"checkout_url":pi.checkout_url}}

@router.get("/{oid}")
def one(oid: str):
    o=get_by_id("orders",oid)
    if not o: raise HTTPException(404,"not found")
    return o

@router.get("")
def by_customer(customer_id: str=""):
    if customer_id: return [o for o in DB["orders"] if o["customer_id"]==customer_id]
    return DB["orders"]

@router.post("/{oid}/status")
async def set_status(oid: str, r: StatusReq):
    try: o=svc().update_status(oid,r.status)
    except ValueError as e: raise HTTPException(400,str(e))
    if r.status=="ON_THE_WAY":
        mp=get_maps()
        route=mp.route(Coords(o["restaurant_lat"],o["restaurant_lng"]),Coords(o["customer_lat"],o["customer_lng"]))
        await simulate_driver(oid,route.polyline)
    from app.tracking.manager import manager
    await manager.broadcast(oid,{"type":"status","order_id":oid,"status":r.status})
    return o