import bcrypt
from fastapi import APIRouter, Form, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from email_validator import validate_email, EmailNotValidError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Настройка конфигурации почты
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def send_email(email: str):
    message = MessageSchema(
        subject="Регистрация прошла успешно",
        recipients=[email],
        body="Поздравляем! Ваша регистрация прошла успешно.",
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),  # Добавлено поле для имени пользователя
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Валидация email
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

    # Проверка на существование email
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("index.html", {"request": request, "error": "Email уже существует."})

    # Хэширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Создание нового пользователя
    new_user = User(username=username, email=email, password=hashed_password)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()  # Откат транзакции в случае ошибки
        return templates.TemplateResponse("index.html", {"request": request, "error": "Ошибка при регистрации пользователя."})

    # Отправка email
    await send_email(email)

    return templates.TemplateResponse("success.html", {"request": request, "email": email})
