from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Restaurant,Order
from app.security import require_roles
router=APIRouter(prefix='/api/restaurant',tags=['restaurant portal'])
@router.get('/orders')
def orders(db:Session=Depends(get_db),u=Depends(require_roles('restaurant','admin'))):
    rs=db.query(Restaurant).filter_by(owner_id=u.id).all() if u.role!='admin' else db.query(Restaurant).all(); ids=[r.id for r in rs]
    return [{'id':o.id,'restaurant_id':o.restaurant_id,'status':o.status,'total':o.total,'created_at':o.created_at.isoformat()} for o in db.query(Order).filter(Order.restaurant_id.in_(ids)).order_by(Order.created_at.desc()).limit(200)]
@router.patch('/orders/{oid}/status')
def status(oid:int,new_status:str,db:Session=Depends(get_db),u=Depends(require_roles('restaurant','admin'))):
    o=db.get(Order,oid)
    if not o: raise HTTPException(404,'Order not found')
    o.status=new_status; db.commit(); return {'ok':True,'status':o.status}
