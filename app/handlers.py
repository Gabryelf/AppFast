import uuid
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from forms import UserForm, UserCreateForm
from models import connect_db, User, AuthToken
from utils import get_password_hash
from auth import check_auth_token

router = APIRouter()

# Настройка шаблонов
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/login')
def login(user_form: UserForm, database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'user or password invalid'}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {
        'token': auth_token.token
    }


@router.post('/user', name='user:create')
def create_user(user: UserCreateForm, database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
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
    return {'id': user.id, 'email': user.email, 'nick_name': user.nick_name}
