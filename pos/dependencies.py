from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from database import get_db
from services.auth_service import get_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token:str=Depends(oauth2_scheme), db:Session= Depends(get_db)):
    user=get_user_from_token(db, token)
    return user

def require_cashier(
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["cashier", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cashier access required",
        )

    return current_user


def require_manager(
    current_user = Depends(get_current_user)
):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required",
        )

    return current_user