
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.usecases.auth import AuthManager
from app.utils.logging import APILogger
from pydantic import BaseModel

router = APIRouter()
auth_manager = AuthManager()
logger = APILogger()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Retorna um token caso o login seja bem sucedido.

    Parâmetros:
    - username: usuário
    - password: senha
    """
    try:
        user = auth_manager.authenticate_user(
            form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=auth_manager.jwt_token_expire_minutes)

        access_token = auth_manager.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(error)}")
