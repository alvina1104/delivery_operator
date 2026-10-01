from datetime import datetime, timedelta
from typing import Optional
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, Query
from passlib.context import CryptContext
from jose import jwt, JWTError
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, RefreshToken
from mysite.database.schema import UserInputSchema, UserOutSchema, UserLoginSchema, UserUpdateSchema, CurrentUserSchema
=======
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from mysite.database.db import SessionLocal
from mysite.database.models import User, RefreshToken
from mysite.schemas.auth_schema import UserRegisterSchema, UserLoginSchema, UserOutSchema, CurrentUserSchema, RefreshTokenSchema
>>>>>>> 79752a4 (chain)
from mysite.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось проверить учетные данные",
    headers={"WWW-Authenticate": "Bearer"}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
<<<<<<< HEAD
auth_router = APIRouter(prefix="/auth", tags=["Auth Tokens"])
=======
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
>>>>>>> 79752a4 (chain)


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
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
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

<<<<<<< HEAD
    current_user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
=======
    current_user = db.query(User).filter(User.id == user_id).first()
>>>>>>> 79752a4 (chain)

    if current_user is None:
        raise credentials_exception

    return current_user


<<<<<<< HEAD
def get_token_data(user: UserProfile):
    return {
        "sub": str(user.id),
        "username": user.username,
        "status": user.status.value
=======
def get_token_data(user: User):
    return {
        "sub": str(user.id),
        "username": user.username
>>>>>>> 79752a4 (chain)
    }


@auth_router.post("/register/", response_model=dict)
<<<<<<< HEAD
async def register(user: UserInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()

    if user_db or email_db:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hash_password = get_password_hash(user.password)

    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=hash_password
=======
async def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    username_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()

    if username_db or email_db:
        raise HTTPException(status_code=400, detail="Username или email уже существует")

    user_data = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=get_password_hash(user.password)
>>>>>>> 79752a4 (chain)
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return {"message": "Пользователь успешно создан"}


@auth_router.post("/login/", response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
<<<<<<< HEAD
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
=======
    user_db = db.query(User).filter(User.username == user.username).first()
>>>>>>> 79752a4 (chain)

    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail="Username или password неправильный")

    token_data = get_token_data(user_db)
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    token_db = RefreshToken(
        user_id=user_db.id,
        token=refresh_token
    )

    db.add(token_db)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


@auth_router.post("/logout/")
<<<<<<< HEAD
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
=======
async def logout(refresh_token: str = Query(...), db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Неверный refresh token")
>>>>>>> 79752a4 (chain)

    db.delete(token_db)
    db.commit()

<<<<<<< HEAD
    return {"message": "User logged out"}


@auth_router.post("/refresh/", response_model=dict)
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
=======
    return {"message": "Пользователь успешно вышел из системы"}


@auth_router.post("/refresh/")
async def refresh(refresh_token: str = Query(...), db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Неверный refresh token")
>>>>>>> 79752a4 (chain)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("token_type") != "refresh":
<<<<<<< HEAD
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user_db = token_db.token_user
    token_data = get_token_data(user_db)
    access_token = create_access_token(token_data)
=======
            raise HTTPException(status_code=401, detail="Неверный тип токена")

    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token недействителен или срок его действия истёк")

    user_db = token_db.token_user
    access_token = create_access_token(get_token_data(user_db))
>>>>>>> 79752a4 (chain)

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

<<<<<<< HEAD

@auth_router.get("/verify/", response_model=CurrentUserSchema)
async def verify(current_user: UserProfile = Depends(get_current_user)):
    return current_user


@auth_router.get("/me/", response_model=UserOutSchema)
async def me(current_user: UserProfile = Depends(get_current_user)):
    return current_user


@auth_router.put("/update/", response_model=UserOutSchema)
async def update(user_in: UserUpdateSchema, current_user: UserProfile = Depends(get_current_user), db: Session = Depends(get_db)):
    update_data = user_in.model_dump(exclude_unset=True)

    if "username" in update_data:
        user_db = db.query(UserProfile).filter(
            UserProfile.username == update_data["username"],
            UserProfile.id != current_user.id
        ).first()

        if user_db:
            raise HTTPException(status_code=400, detail="Пользователь с таким username уже существует")

    if "email" in update_data:
        email_db = db.query(UserProfile).filter(
            UserProfile.email == update_data["email"],
            UserProfile.id != current_user.id
        ).first()

        if email_db:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@auth_router.delete("/delete/", response_model=dict)
async def delete(current_user: UserProfile = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()

    return {"message": "Пользователь успешно удалено"}
=======
@auth_router.get("/me/", response_model=UserOutSchema)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get("/verify/", response_model=CurrentUserSchema)
async def verify(current_user: User = Depends(get_current_user)):
    return current_user
>>>>>>> 79752a4 (chain)
