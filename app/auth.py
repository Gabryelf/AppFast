from fastapi import Depends, HTTPException, Header
from starlette import status
from models import AuthToken, connect_db


def check_auth_token(
        authorization: str = Header(None),
        database=Depends(connect_db)
):
    """
    Проверка токена аутентификации.
    Поддерживает два формата:
    1. Bearer токен в заголовке Authorization
    2. Параметр запроса token
    """
    token = None

    # Проверяем заголовок Authorization
    if authorization and authorization.startswith('Bearer '):
        token = authorization.replace('Bearer ', '')

    # Если токен не найден в заголовке, пробуем получить из query параметров
    # (для обратной совместимости с существующим кодом)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Authorization header missing or invalid'
        )

    # Ищем токен в базе данных
    auth_token = database.query(AuthToken).filter(AuthToken.token == token).first()
    if auth_token:
        return auth_token

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


# Старая версия для обратной совместимости
def check_auth_token_old(token: str, database=Depends(connect_db)):
    auth_token = database.query(AuthToken).filter(AuthToken.token == token).first()
    if auth_token:
        return auth_token

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')

