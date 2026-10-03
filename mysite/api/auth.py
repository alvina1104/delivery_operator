from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from mysite.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, RefreshToken
from mysite.schemas.auth_schema import UserRegisterSchema, UserLoginSchema, UserOutSchema, CurrentUserSchema

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Не удалось проверить учетные данные", headers={"WWW-Authenticate": "Bearer"})
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_LIFETIME)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "access":
            raise credentials_exception
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception
    current_user = db.query(User).filter(User.id == user_id).first()
    if current_user is None:
        raise credentials_exception
    return current_user

def get_token_data(user: User):
    return {"sub": str(user.id), "username": user.username}

@auth_router.post("/register/", response_model=dict)
async def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    username_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()
    if username_db or email_db:
        raise HTTPException(status_code=400, detail="Username или email уже существует")
    user_data = User(username=user.username, email=user.email, phone_number=user.phone_number, password=get_password_hash(user.password))
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {"message": "Пользователь успешно создан"}

@auth_router.post("/login/", response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail="Username или password неправильный")
    token_data = get_token_data(user_db)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    db.add(RefreshToken(user_id=user_db.id, token=refresh_token))
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

@auth_router.post("/logout/")
async def logout(refresh_token: str = Query(...), db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_db:
        raise HTTPException(status_code=401, detail="Неверный refresh token")
    db.delete(token_db)
    db.commit()
    return {"message": "Пользователь успешно вышел из системы"}

@auth_router.post("/refresh/")
async def refresh(refresh_token: str = Query(...), db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_db:
        raise HTTPException(status_code=401, detail="Неверный refresh token")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Неверный тип токена")
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token недействителен или срок его действия истёк")
    access_token = create_access_token(get_token_data(token_db.token_user))
    return {"access_token": access_token, "token_type": "Bearer"}

@auth_router.get("/me/", response_model=UserOutSchema)
async def me(current_user: User = Depends(get_current_user)):
    return current_user

@auth_router.get("/verify/", response_model=CurrentUserSchema)
async def verify(current_user: User = Depends(get_current_user)):
    return current_user