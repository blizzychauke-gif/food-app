from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import User

pwd=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2=OAuth2PasswordBearer(tokenUrl='/api/auth/login')

def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(user):
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    return jwt.encode({'sub':str(user.id),'role':user.role,'exp':exp},settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)

def current_user(token: str=Depends(oauth2), db: Session=Depends(get_db)):
    cred=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication credentials', headers={'WWW-Authenticate':'Bearer'})
    try:
        payload=jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.JWT_ALGORITHM]); uid=int(payload['sub'])
    except (JWTError,KeyError,ValueError): raise cred
    user=db.get(User,uid)
    if not user or not user.is_active: raise cred
    return user

def require_roles(*roles):
    def dep(user=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403,'Insufficient permissions')
        return user
    return dep
