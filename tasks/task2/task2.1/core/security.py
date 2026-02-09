import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from datetime import datetime, timedelta
import uuid
import os
import time

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

blacklist_store = {}

class Auth:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def _create_token(self, data: dict, expires_delta: timedelta, token_type: str):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire, "jti": str(uuid.uuid4()), "type": token_type})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_access_token(self, data: dict):
        return self._create_token(data, timedelta(minutes=15), "access")

    def create_refresh_token(self, data: dict):
        return self._create_token(data, timedelta(days=7), "refresh")

    def _decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен недействителен")

    def verify_access_token(self, token: str = Security(api_key_header)):
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Token отсутствует.")
        if token.startswith("Bearer "):
            token = token[7:]

        payload = self._decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Это не Access Token.")
        
        jti = payload.get("jti")
        if jti in blacklist_store and blacklist_store[jti] > time.time():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Token отозван.")
        return payload

    def verify_refresh_token(self, token: str):
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh Token отсутствует.")

        payload = self._decode_token(token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Это не Refresh Token.")
        
        jti = payload.get("jti")
        if jti in blacklist_store and blacklist_store[jti] > time.time():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token отозван.")
        return payload

    def add_to_blacklist(self, jti: str, exp_timestamp: float):
        if exp_timestamp > time.time():
            blacklist_store[jti] = exp_timestamp

auth = Auth(SECRET_KEY, ALGORITHM)