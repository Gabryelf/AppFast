from fastapi import Depends, HTTPException, Header
from app.database import AuthToken, connect_db


def check_auth_token(
    authorization: str = Header(None),
    db=Depends(connect_db)
):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')

    token = authorization.replace('Bearer ', '')
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).first()

    if not auth_token:
        raise HTTPException(status_code=401, detail='Invalid token')

    return auth_token