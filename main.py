from fastapi import FastAPI, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List
import models, schemas, database
from datetime import datetime
import uvicorn
# Create FastAPI instance
app = FastAPI()
# Auto-create tables
models.Base.metadata.create_all(bind=database.engine)
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Hashing password
def get_password_hash(password):
    return pwd_context.hash(password)
# Verifying password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# Create user
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        created_at=datetime.utcnow(),
        login_count=0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Read all users
@app.get("/users/", response_model=List[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
# Read a single user by ID
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# Update a user
@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = user_update.name
    user.email = user_update.email
    user.password = get_password_hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user
# Delete a user
@app.delete("/users/{user_id}", response_model=schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user
# Login (with session login count update)
@app.post("/token")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user.login_count += 1
    db.commit()
    return {"message": f"Welcome {user.name}!", "login_count": user.login_count}
# Fetch first user
@app.get("/users/me", response_model=schemas.UserOut)
def read_current_user(db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user
# Start FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
