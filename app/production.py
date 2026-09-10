from app.db import engine, Base, SessionLocal
from app.models import User
from app.security import hash_password

def init_db():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        admin_email='admin@fooddash.local'
        if not db.query(User).filter_by(email=admin_email).first():
            db.add(User(email=admin_email,password_hash=hash_password('ChangeMe123!'),full_name='FoodDash Admin',role='admin'))
            db.commit()
    finally: db.close()
