from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Driver,Order
from app.security import require_roles
router=APIRouter(prefix='/api/driver',tags=['driver'])
class GPS(BaseModel): lat:float; lng:float
@router.get('/orders')
def orders(db:Session=Depends(get_db),u=Depends(require_roles('driver','admin'))):
    d=db.query(Driver).filter_by(user_id=u.id).first() if u.role!='admin' else None
    q=db.query(Order) if u.role=='admin' else db.query(Order).filter(Order.driver_id==d.id)
    return [{'id':o.id,'status':o.status,'total':o.total,'lat':o.lat,'lng':o.lng} for o in q.order_by(Order.created_at.desc()).limit(100)]
@router.post('/location')
def location(p:GPS,db:Session=Depends(get_db),u=Depends(require_roles('driver','admin'))):
    d=db.query(Driver).filter_by(user_id=u.id).first()
    if not d: raise HTTPException(404,'Driver profile not found')
    d.lat,d.lng,d.updated_at=p.lat,p.lng,datetime.utcnow(); d.status='online'; db.commit()
    return {'ok':True,'lat':p.lat,'lng':p.lng,'updated_at':d.updated_at.isoformat()}
@router.post('/orders/{oid}/accept')
def accept(oid:int,db:Session=Depends(get_db),u=Depends(require_roles('driver','admin'))):
    d=db.query(Driver).filter_by(user_id=u.id).first(); o=db.get(Order,oid)
    if not o: raise HTTPException(404,'Order not found')
    o.driver_id=d.id; o.status='ACCEPTED'; db.commit(); return {'ok':True}
