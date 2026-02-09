from fastapi import APIRouter, Depends, HTTPException, Path, Security, Body
from sqlalchemy.orm import Session
import time 
import requests

from schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserSchema,
    UserInfoSchema,
    UserLoginResponseSchema,
)

from services.user_services import (
    UserCreateManager,
    UserLoginManager,
)
from core.database import get_db
from core.security import auth

router = APIRouter()


@router.post("/signup", response_model=UserSchema)
async def create_user(
    new_user: UserCreateSchema = Body(...), db: Session = Depends(get_db)
):
    user = UserCreateManager(db).create_user(new_user)
    return user


@router.post("/signin", response_model=UserLoginResponseSchema)
async def login(creds: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    user = UserLoginManager(db).login_user(creds.username, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    token_values = {"username": user.username, "id": user.id}
    return {
        "access_token": auth.create_access_token(token_values),
        "token_type": "bearer",
    }


@router.get("/info", response_model=UserInfoSchema)
async def get_info(
    payload: dict = Depends(auth.verify_access_token),
):
    if not payload:
        return {"status_code": 401, "message": "вы не авторизованы"}
    user_id = payload.get("id")
    return {"id": user_id, "type_id": str(type(user_id))}

@router.get("/latency")
def ping_google():
    url = "https://google.com"
    try:
        start_time = time.time()
        
        response = requests.get(url, allow_redirects=True, timeout=10)
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        return {
            "destination": url,
            "http_status_code": response.status_code,
            "latency_ms": latency_ms,
            "success": True
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка HTTP запроса до {url}: {str(e)}")


@router.post("/logout")
async def logout(payload: dict = Security(auth.verify_access_token)):
    auth.add_to_blacklist(payload["jti"], payload["exp"])

    return {"message": "Вы успешно вышли из системы. Ваш Access Token отозван."}