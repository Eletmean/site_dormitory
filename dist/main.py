from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dist.database import SessionLocal  # Импорт сессии базы данных
from dist.models import User
from passlib.context import CryptContext
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="src")

# Подключаем статические файлы из папки "styles" внутри "src"
app.mount("/styles", StaticFiles(directory="src/styles"), name="styles")
app.mount("/images", StaticFiles(directory="src/images"), name="images")
app.mount("/js", StaticFiles(directory="src/js"), name="js")

# Инициализация хеширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/register")

@app.get("/register", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    fullName: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    studyGroup: str = Form(...),
    passport: str = Form(...),
    roomType: str = Form(...),
    building: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверка на существование email
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # Проверка на наличие слова "Владивосток" в адресе
    if "Владивосток" in address:
        raise HTTPException(status_code=400, detail="Прописка в черте города недопустима")

    # Хеширование пароля
    hashed_password = pwd_context.hash(password)

    # Создание нового пользователя
    new_user = User(
        full_name=fullName,
        email=email,
        address=address,
        study_group=studyGroup,
        passport=passport,
        room_type=roomType,
        building=building,
        password=hashed_password  # Сохранение хешированного пароля
    )
    
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        # Запись данных пользователя в Excel после успешной регистрации
        save_to_excel(new_user)
    except Exception as e:
        db.rollback()  # Откат транзакции в случае ошибки
        raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")

    # Перенаправление на страницу успешной регистрации
    return RedirectResponse(url="/success", status_code=303)

# Путь к файлу Excel
EXCEL_FILE_PATH = "C:/Users/elina/OneDrive/Рабочий стол/hotelusers.xlsx"

def save_to_excel(user: User):
    # Создание DataFrame в зависимости от наличия файла
    if os.path.exists(EXCEL_FILE_PATH):
        # Если файл уже существует, добавляем новые данные
        df = pd.read_excel(EXCEL_FILE_PATH)
        new_data = {
            "Полное имя": [user.full_name],
            "Email": [user.email],
            "Адрес": [user.address],
            "Учебная группа": [user.study_group],
            "Паспорт": [user.passport],
            "Тип комнаты": [user.room_type],
            "Здание": [user.building],
        }
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
    else:
        # Если файла нет, создаем новый DataFrame
        new_data = {
            "Полное имя": [user.full_name],
            "Email": [user.email],
            "Адрес": [user.address],
            "Учебная группа": [user.study_group],
            "Паспорт": [user.passport],
            "Тип комнаты": [user.room_type],
            "Здание": [user.building],
        }
        df = pd.DataFrame(new_data)

    # Сохраняем в Excel, создаем или обновляем файл
    with pd.ExcelWriter(EXCEL_FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Users', index=False)

@app.get("/export", response_class=FileResponse)
async def export_to_excel(db: Session = Depends(get_db)):
    # Извлечение данных пользователей из базы данных
    users = db.query(User).all()

    # Если таблица пуста, сообщите об этом
    if not users:
        raise HTTPException(status_code=404, detail="Нет данных для экспорта")

    # Преобразование данных в DataFrame
    user_data = {
        "Полное имя": [user.full_name for user in users],
        "Email": [user.email for user in users],
        "Адрес": [user.address for user in users],
        "Учебная группа": [user.study_group for user in users],
        "Паспорт": [user.passport for user in users],
        "Тип комнаты": [user.room_type for user in users],
        "Здание": [user.building for user in users],
    }

    df = pd.DataFrame(user_data)

    # Запись данных в файл
    df.to_excel(EXCEL_FILE_PATH, index=False, sheet_name='Users')

    return FileResponse(EXCEL_FILE_PATH, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='exported_data.xlsx')

@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/propiska", response_class=HTMLResponse)
async def propiska_page(request: Request):
    return templates.TemplateResponse("propiska.html", {"request": request})

@app.get("/wrongemail", response_class=HTMLResponse)
async def wrong_email_page(request: Request):
    return templates.TemplateResponse("wrongemail.html", {"request": request})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 400:
        if "Пользователь с таким email уже существует" in exc.detail:
            return await wrong_email_page(request)
        elif "Прописка в черте города недопустима" in exc.detail:
            return await propiska_page(request)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)

@app.get("/korpuss", response_class=HTMLResponse)
async def get_korpuss_page(request: Request):
    return templates.TemplateResponse("korpuss.html", {"request": request})

@app.get("/rooms", response_class=HTMLResponse)
async def get_rooms_page(request: Request):
    return templates.TemplateResponse("rooms.html", {"request": request})

# Маршрут для проверки доступных маршрутов
@app.get("/routes")
async def get_routes():
    return {"routes": [route.path for route in app.routes]}