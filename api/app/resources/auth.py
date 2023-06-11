
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.usecases.auth import AuthManager
from app.utils.logging import logger
from pydantic import BaseModel

router = APIRouter()
auth_manager = AuthManager()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Returns a token if the login is successful.

    Parameters:
    - username: username string
    - password: password string
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
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as error:
        raise error
    except Exception as error:
        error_msg = f"Create access token internal server error: {str(error)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500, detail=error_msg)
