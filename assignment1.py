from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import h3
import queue
import threading
from datetime import datetime

app = FastAPI()

engine = create_engine("sqlite:///azhar.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    h3_index = Column(String)

class HelpRequest(Base):
    __tablename__ = "help_requests"
    id = Column(Integer, primary_key=True)
    recipient_id = Column(Integer)
    description = Column(String)
    status = Column(String, default="pending")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_role(required_role: str):
    def role_checker(x_user_role: str = Header(...)):
        if x_user_role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return x_user_role
    return role_checker

event_queue = queue.Queue()

def audit_worker():
    while True:
        event_data = event_queue.get()
        db = SessionLocal()
        new_log = AuditLog(action=event_data)
        db.add(new_log)
        db.commit()
        db.close()
        event_queue.task_done()

threading.Thread(target=audit_worker, daemon=True).start()


@app.post("/users/register")
def register_user(name: str, role: str, lat: float, lon: float, db: Session = Depends(get_db)):
    h3_idx = h3.geo_to_h3(lat, lon, 7)
    user = User(name=name, role=role, h3_index=h3_idx)
    db.add(user)
    db.commit()
    event_queue.put(f"User {name} registered with role {role}")
    return {"status": "created", "h3_index": h3_idx}

@app.post("/requests/create")
def create_request(desc: str, db: Session = Depends(get_db), role: str = Depends(verify_role("recipient"))):
    new_req = HelpRequest(description=desc, recipient_id=1)
    db.add(new_req)
    db.commit()
    return {"message": "Request submitted"}

@app.patch("/requests/verify/{req_id}")
def verify_request(req_id: int, db: Session = Depends(get_db), role: str = Depends(verify_role("admin"))):
    req = db.query(HelpRequest).filter(HelpRequest.id == req_id).first()
    if not req: raise HTTPException(status_code=404)
    req.status = "verified"
    db.commit()
    event_queue.put(f"Admin verified request {req_id}")
    return {"status": "verified"}

@app.get("/analytics/region/{h3_index}")
def get_regional_stats(h3_index: str, db: Session = Depends(get_db)):
    count = db.query(User).filter(User.h3_index == h3_index).count()
    return {"h3_index": h3_index, "total_users": count}

@app.get("/system/logs")
def view_logs(db: Session = Depends(get_db), role: str = Depends(verify_role("admin"))):
    return db.query(AuditLog).all()