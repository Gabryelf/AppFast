from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import (
    UserLogin, UserCreate, UserResponse, TokenResponse,
    ItemCreate, ItemUpdate, ItemResponse, ItemsListResponse
)
from app.database import get_db, User, Item, AuthToken
from app.auth import authenticate_user, create_auth_token, get_current_user
from app.utils import format_images, get_password_hash

router = APIRouter(tags=["API"])


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Вход в систему"""
    user = authenticate_user(user_data.email, user_data.password, db)
    token = create_auth_token(user.id, db)

    return TokenResponse(
        message="Успешный вход в систему",
        token=token
    )


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    print(f"🔍 Attempting to register user: {user_data.email}")

    try:
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )

        # Создаем нового пользователя
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

        print(f"✅ User created with ID: {user.id}")

        # Создаем токен
        token = create_auth_token(user.id, db)

        return TokenResponse(
            message="Пользователь успешно создан",
            token=token
        )

    except Exception as e:
        print(f"❌ Error in register: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при регистрации: {str(e)}"
        )


@router.get("/user", response_model=UserResponse)
async def get_user(user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        nick_name=user.nick_name,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Выход из системы"""
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
    """Создание нового предмета"""
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

    # Получаем список изображений
    images_list = []
    if item.images:
        import json
        try:
            images_list = json.loads(item.images)
        except:
            images_list = []

    return ItemResponse(
        id=item.id,
        user_id=item.user_id,
        title=item.title,
        description=item.description,
        cover_image=item.cover_image,
        images=images_list,
        created_at=item.created_at
    )


@router.get("/items", response_model=ItemsListResponse)
async def list_items(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db)
):
    """Получение списка предметов"""
    items = db.query(Item).order_by(Item.created_at.desc()).offset(skip).limit(limit).all()

    items_list = []
    for item in items:
        images_list = []
        if item.images:
            import json
            try:
                images_list = json.loads(item.images)
            except:
                images_list = []

        items_list.append(ItemResponse(
            id=item.id,
            user_id=item.user_id,
            title=item.title,
            description=item.description,
            cover_image=item.cover_image,
            images=images_list,
            created_at=item.created_at
        ))

    return ItemsListResponse(
        items=items_list,
        count=len(items_list),
        message="Список предметов"
    )


@router.get("/items/my", response_model=ItemsListResponse)
async def my_items(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Получение предметов текущего пользователя"""
    items = db.query(Item).filter(
        Item.user_id == current_user.id
    ).order_by(Item.created_at.desc()).all()

    items_list = []
    for item in items:
        images_list = []
        if item.images:
            import json
            try:
                images_list = json.loads(item.images)
            except:
                images_list = []

        items_list.append(ItemResponse(
            id=item.id,
            user_id=item.user_id,
            title=item.title,
            description=item.description,
            cover_image=item.cover_image,
            images=images_list,
            created_at=item.created_at
        ))

    return ItemsListResponse(
        items=items_list,
        count=len(items_list),
        message="Мои предметы"
    )


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Получение предмета по ID"""
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предмет не найден"
        )

    images_list = []
    if item.images:
        import json
        try:
            images_list = json.loads(item.images)
        except:
            images_list = []

    return ItemResponse(
        id=item.id,
        user_id=item.user_id,
        title=item.title,
        description=item.description,
        cover_image=item.cover_image,
        images=images_list,
        created_at=item.created_at
    )


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

    # Обновляем поля
    if item_data.title is not None:
        item.title = item_data.title
    if item_data.description is not None:
        item.description = item_data.description
    if item_data.cover_image is not None:
        item.cover_image = item_data.cover_image
    if item_data.images is not None:
        item.images = format_images(item_data.images)

    db.commit()
    db.refresh(item)

    images_list = []
    if item.images:
        import json
        try:
            images_list = json.loads(item.images)
        except:
            images_list = []

    return ItemResponse(
        id=item.id,
        user_id=item.user_id,
        title=item.title,
        description=item.description,
        cover_image=item.cover_image,
        images=images_list,
        created_at=item.created_at
    )


@router.delete("/items/{item_id}")
async def delete_item(
        item_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Удаление предмета"""
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