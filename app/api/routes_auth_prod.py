from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.security import hash_password, verify_password, create_token, current_user

router=APIRouter(prefix='/api/auth',tags=['authentication'])
class Register(BaseModel): email: EmailStr; password: str; full_name: str; phone: str|None=None
class Login(BaseModel): email: EmailStr; password: str
@router.post('/register')
def register(r:Register,db:Session=Depends(get_db)):
    if len(r.password)<8: raise HTTPException(400,'Password must be at least 8 characters')
    if db.query(User).filter_by(email=r.email.lower()).first(): raise HTTPException(409,'Email already registered')
    u=User(email=r.email.lower(),password_hash=hash_password(r.password),full_name=r.full_name,phone=r.phone)
    db.add(u); db.commit(); db.refresh(u)
    return {'access_token':create_token(u),'token_type':'bearer','user':{'id':u.id,'email':u.email,'name':u.full_name,'role':u.role}}
@router.post('/login')
def login(r:Login,db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=r.email.lower()).first()
    if not u or not verify_password(r.password,u.password_hash): raise HTTPException(401,'Incorrect email or password')
    return {'access_token':create_token(u),'token_type':'bearer','user':{'id':u.id,'email':u.email,'name':u.full_name,'role':u.role}}
@router.get('/me')
def me(u=Depends(current_user)): return {'id':u.id,'email':u.email,'name':u.full_name,'phone':u.phone,'role':u.role}
