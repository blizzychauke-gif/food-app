from fastapi import APIRouter
from pydantic import BaseModel
from app.deps import get_maps
from app.providers.maps.interface import Coords
router=APIRouter(prefix="/api/maps",tags=["maps"])
class RouteReq(BaseModel):
    o_lat: float; o_lng: float; d_lat: float; d_lng: float
@router.get("/autocomplete")
def auto(query: str=""): return [p.__dict__ for p in get_maps().autocomplete(query)]
@router.get("/geocode")
def geo(address: str=""):
    c=get_maps().geocode(address); return {"lat":c.lat,"lng":c.lng} if c else {"error":"not found"}
@router.get("/reverse")
def rev(lat: float=0,lng: float=0): return {"address": get_maps().reverse_geocode(lat,lng)}
@router.post("/route")
def route(r: RouteReq):
    info=get_maps().route(Coords(r.o_lat,r.o_lng),Coords(r.d_lat,r.d_lng))
    return {"distance_km":info.distance_km,"eta_min":info.eta_min,"polyline":info.polyline}