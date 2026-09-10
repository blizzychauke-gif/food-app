from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User,Order,Restaurant,Driver
from app.security import require_roles
router=APIRouter(prefix='/api/admin',tags=['admin'])
@router.get('/dashboard')
def dashboard(db:Session=Depends(get_db),_=Depends(require_roles('admin'))):
    return {'customers':db.query(User).filter_by(role='customer').count(),'restaurants':db.query(Restaurant).count(),'drivers':db.query(Driver).count(),'orders':db.query(Order).count(),'revenue':round(db.query(func.coalesce(func.sum(Order.total),0)).scalar() or 0,2)}
@router.get('/users')
def users(db:Session=Depends(get_db),_=Depends(require_roles('admin'))): return [{'id':u.id,'email':u.email,'name':u.full_name,'role':u.role,'active':u.is_active} for u in db.query(User).order_by(User.id.desc()).limit(200)]
@router.patch('/users/{uid}/role')
def role(uid:int, role:str,db:Session=Depends(get_db),_=Depends(require_roles('admin'))):
    u=db.get(User,uid); u.role=role; db.commit(); return {'ok':True}
