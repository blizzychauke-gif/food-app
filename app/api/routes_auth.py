from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.deps import get_otp
router=APIRouter(prefix="/api/auth",tags=["auth"])
class SendReq(BaseModel): phone: str
class VerifyReq(BaseModel): phone: str; code: str
@router.post("/otp/send")
def send(r: SendReq): return get_otp().send_otp(r.phone)
@router.post("/otp/resend")
def resend(r: SendReq): return get_otp().resend_otp(r.phone)
@router.post("/otp/verify")
def verify(r: VerifyReq):
    try:
        ok=get_otp().verify_otp(r.phone,r.code)
    except ValueError as e: raise HTTPException(400,str(e))
    if not ok: raise HTTPException(400,"Incorrect OTP")
    return {"verified":True,"phone":r.phone}