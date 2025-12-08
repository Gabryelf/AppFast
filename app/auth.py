from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db, AuthToken, User
from app.utils import get_password_hash
from sqlalchemy.orm import Session

security = HTTPBearer()


def authenticate_user(email: str, password: str, db: Session) -> User:
    """Аутентификация пользователя"""
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )

    # Проверяем пароль
    hashed_password = get_password_hash(password)
    if user.password != hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )

    return user


def create_auth_token(user_id: int, db: Session) -> str:
    token = AuthToken.generate_token()
    auth_token = AuthToken(token=token, user_id=user_id)

    db.add(auth_token)
    db.commit()

    return token


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    auth_token = db.query(AuthToken).filter(AuthToken.token == token).first()
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен аутентификации"
        )

    user = db.query(User).filter(User.id == auth_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    return user
