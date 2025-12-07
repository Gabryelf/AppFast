from fastapi import Depends, HTTPException, Header
from starlette import status
from app.models import AuthToken, connect_db


def check_auth_token(
        authorization: str = Header(None),
        database=Depends(connect_db)
):
    """Проверка токена аутентификации"""
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Authorization header missing or invalid'
        )

    token = authorization.replace('Bearer ', '')
    auth_token = database.query(AuthToken).filter(AuthToken.token == token).first()

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )

    return auth_token
