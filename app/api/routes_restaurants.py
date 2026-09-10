from fastapi import APIRouter, HTTPException
from app.store import DB, get_by_id
router=APIRouter(prefix="/api/restaurants",tags=["restaurants"])
@router.get("")
def list_all(search: str=""):
    if not search: return DB["restaurants"]
    s=search.lower(); return [r for r in DB["restaurants"] if s in r["name"].lower() or s in r["cuisine"].lower()]
@router.get("/{rid}")
def one(rid: str):
    r=get_by_id("restaurants",rid)
    if not r: raise HTTPException(404,"not found")
    return r
@router.get("/{rid}/menu")
def menu(rid: str):
    return [f for f in DB["foods"] if f["restaurant_id"]==rid]