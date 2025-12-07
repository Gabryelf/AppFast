import json
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from forms import UserForm, UserCreateForm, ItemCreateForm, ItemUpdateForm
from models import connect_db, User, AuthToken, Item
from utils import get_password_hash
from auth import check_auth_token

from config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/items", response_class=HTMLResponse)
async def get_items_page(request: Request):
    return templates.TemplateResponse("items.html", {"request": request})


# Аутентификация
@router.post('/login')
def login(user_form: UserForm, database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).first()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'user or password invalid'}

    auth_token = AuthToken(
        token=AuthToken.generate_token(),
        user_id=user.id
    )
    database.add(auth_token)
    database.commit()
    return {'token': auth_token.token}


@router.post('/user', name='user:create')
def create_user(user: UserCreateForm, database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(User.email == user.email).first()
    if exists_user:
        raise HTTPException(status_code=400, detail='Email already exists')

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        nick_name=user.nick_name
    )
    database.add(new_user)
    database.commit()
    return {'user_id': new_user.id}


@router.get('/user', name='user:get')
def get_user(auth_token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == auth_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return {
        'id': user.id,
        'email': user.email,
        'nick_name': user.nick_name,
        'first_name': user.first_name,
        'last_name': user.last_name
    }


@router.post('/logout', name='user:logout')
def logout(authorization: str = Header(None), database=Depends(connect_db)):
    if authorization and authorization.startswith('Bearer '):
        token = authorization.replace('Bearer ', '')
        auth_token = database.query(AuthToken).filter(AuthToken.token == token).first()
        if auth_token:
            database.delete(auth_token)
            database.commit()

    return {'message': 'Logged out successfully'}


# Item CRUD операции
@router.post('/items', name='item:create')
def create_item(
        item: ItemCreateForm,
        auth_token: AuthToken = Depends(check_auth_token),
        database=Depends(connect_db)
):
    new_item = Item(
        user_id=auth_token.user_id,
        title=item.title,
        description=item.description,
        cover_image=item.cover_image,
        images=json.dumps(item.images or []) if item.images else None
    )
    database.add(new_item)
    database.commit()
    database.refresh(new_item)

    return {
        'id': new_item.id,
        'title': new_item.title,
        'description': new_item.description,
        'cover_image': new_item.cover_image,
        'images': json.loads(new_item.images) if new_item.images else []
    }


@router.get('/items', name='item:list')
def list_items(database=Depends(connect_db), limit: int = 50, offset: int = 0):
    items = database.query(Item).order_by(Item.created_at.desc()).limit(limit).offset(offset).all()

    result = []
    for item in items:
        user = database.query(User).filter(User.id == item.user_id).first()
        result.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'cover_image': item.cover_image,
            'images': json.loads(item.images) if item.images else [],
            'created_at': item.created_at,
            'author': {
                'id': user.id,
                'nick_name': user.nick_name,
                'email': user.email
            } if user else None
        })

    return {'items': result, 'count': len(result)}


@router.get('/items/my', name='item:my')
def my_items(
        auth_token: AuthToken = Depends(check_auth_token),
        database=Depends(connect_db)
):
    items = database.query(Item).filter(Item.user_id == auth_token.user_id).order_by(Item.created_at.desc()).all()

    result = []
    for item in items:
        result.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'cover_image': item.cover_image,
            'images': json.loads(item.images) if item.images else [],
            'created_at': item.created_at
        })

    return {'items': result}


@router.get('/items/{item_id}', name='item:get')
def get_item(item_id: int, database=Depends(connect_db)):
    item = database.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')

    user = database.query(User).filter(User.id == item.user_id).first()

    return {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'cover_image': item.cover_image,
        'images': json.loads(item.images) if item.images else [],
        'created_at': item.created_at,
        'author': {
            'id': user.id,
            'nick_name': user.nick_name,
            'email': user.email
        } if user else None
    }


@router.put('/items/{item_id}', name='item:update')
def update_item(
        item_id: int,
        item_update: ItemUpdateForm,
        auth_token: AuthToken = Depends(check_auth_token),
        database=Depends(connect_db)
):
    item = database.query(Item).filter(
        Item.id == item_id,
        Item.user_id == auth_token.user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail='Item not found or access denied')

    if item_update.title is not None:
        item.title = item_update.title
    if item_update.description is not None:
        item.description = item_update.description
    if item_update.cover_image is not None:
        item.cover_image = item_update.cover_image
    if item_update.images is not None:
        item.images = json.dumps(item_update.images)

    database.commit()
    database.refresh(item)

    return {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'cover_image': item.cover_image,
        'images': json.loads(item.images) if item.images else []
    }


@router.delete('/items/{item_id}', name='item:delete')
def delete_item(
        item_id: int,
        auth_token: AuthToken = Depends(check_auth_token),
        database=Depends(connect_db)
):
    item = database.query(Item).filter(
        Item.id == item_id,
        Item.user_id == auth_token.user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail='Item not found or access denied')

    database.delete(item)
    database.commit()

    return {'message': 'Item deleted successfully'}
