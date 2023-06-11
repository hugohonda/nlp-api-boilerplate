from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()


fake_users_db = {
    "teste": {
        "username": "teste",
        "full_name": "Teste Teste",
        "email": "teste@example.com",
        "hashed_password": "$2b$12$dcU.TRVClCu.390jYXDTdeJb/KjNYB/PcOj/ihmDyOj2G/GWeUHlW",
        "disabled": False,
    }
}


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthManager:
    def __init__(self):
        self.jwt_key = os.environ.get('JWT_SECRET_KEY', 'changeme')
        self.jwt_algorithm = os.environ.get('JWT_ALGORITHM', 'HS256')
        self.jwt_token_expire_minutes = int(
            os.environ.get('JWT_TOKEN_EXPIRE_MINUTES', 120))

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def get_user(self, username: str):
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.jwt_key, algorithm=self.jwt_algorithm)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.jwt_key,
                                 algorithms=[self.jwt_algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self,
                                      current_user: Annotated[User, Depends(
                                          get_current_user)]
                                      ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
