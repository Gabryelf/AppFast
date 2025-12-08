from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import (
    UserLogin, UserCreate, UserResponse, TokenResponse,
    ItemCreate, ItemUpdate, ItemResponse, ItemsListResponse
)
from app.database import Session, get_db, User, Item, AuthToken
from app.auth import authenticate_user, create_auth_token, get_current_user
from app.utils import format_images

router = APIRouter(tags=["API"])


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)
    token = create_auth_token(user.id, db)

    return TokenResponse(message="Успешный вход", token=token)


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    from app.utils import get_password_hash

    user = User(
        email=user_data.email,
        password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        nick_name=user_data.nick_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_auth_token(user.id, db)

    return TokenResponse(message="Пользователь создан", token=token)


@router.get("/user", response_model=UserResponse)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post("/logout", response_model=dict)
async def logout(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db.query(AuthToken).filter(AuthToken.user_id == current_user.id).delete()
    db.commit()

    return {"message": "Успешный выход из системы"}


# CRUD для предметов
@router.post("/items", response_model=ItemResponse)
async def create_item(
        item_data: ItemCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    item = Item(
        user_id=current_user.id,
        title=item_data.title,
        description=item_data.description,
        cover_image=item_data.cover_image,
        images=format_images(item_data.images)
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("/items", response_model=ItemsListResponse)
async def list_items(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db)
):
    items = db.query(Item).order_by(Item.created_at.desc()).offset(skip).limit(limit).all()

    return ItemsListResponse(
        items=items,
        count=len(items),
        message="Список предметов"
    )


@router.get("/items/my", response_model=ItemsListResponse)
async def my_items(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    items = db.query(Item).filter(Item.user_id == current_user.id).order_by(Item.created_at.desc()).all()
    return ItemsListResponse(items=items, count=len(items), message="Мои предметы")


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предмет не найден"
        )

    return item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
        item_id: int,
        item_data: ItemUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Обновление предмета"""
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предмет не найден или нет доступа"
        )

    update_data = item_data.dict(exclude_unset=True)

    if "title" in update_data:
        item.title = update_data["title"]
    if "description" in update_data:
        item.description = update_data["description"]
    if "cover_image" in update_data:
        item.cover_image = update_data["cover_image"]
    if "images" in update_data and update_data["images"] is not None:
        item.images = format_images(update_data["images"])

    db.commit()
    db.refresh(item)

    return item


@router.delete("/items/{item_id}")
async def delete_item(
        item_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предмет не найден или нет доступа"
        )

    db.delete(item)
    db.commit()

    return {"message": "Предмет успешно удален"}
