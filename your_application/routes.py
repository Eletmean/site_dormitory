from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from .database import get_connection  # Импортируйте вашу функцию подключения

router = APIRouter()
templates = Jinja2Templates(directory="src")

# Инициализация хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/register")

@router.get("/register", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    fullName: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    studyGroup: str = Form(...),
    passport: str = Form(...),
    roomType: str = Form(...),
    building: str = Form(...),
    password: str = Form(...),  # Добавлено поле для пароля
):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка на существование email
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_email = cursor.fetchone()
            if existing_email:
                raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

            # Проверка на наличие слова "Владивосток" в адресе
            if "Владивосток" in address:
                raise HTTPException(status_code=400, detail="Прописка в черте города недопустима")

            # Хеширование пароля
            hashed_password = pwd_context.hash(password)

            # Создание нового пользователя
            cursor.execute(
                "INSERT INTO users (full_name, email, address, study_group, passport, room_type, building, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (fullName, email, address, studyGroup, passport, roomType, building, hashed_password)
            )
            connection.commit()
    except Exception as e:
        connection.rollback()  # Откат транзакции в случае ошибки
        raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")
    finally:
        connection.close()

    # Перенаправление на страницу успешной регистрации
    return RedirectResponse(url="/success", status_code=303)

@router.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@router.get("/propiska", response_class=HTMLResponse)
async def propiska_page(request: Request):
    return templates.TemplateResponse("propiska.html", {"request": request})

@router.get("/wrongemail", response_class=HTMLResponse)
async def wrong_email_page(request: Request):
    return templates.TemplateResponse("wrongemail.html", {"request": request})

@router.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 400:
        if "Пользователь с таким email уже существует" in exc.detail:
            return await wrong_email_page(request)
        elif "Прописка в черте города недопустима" in exc.detail:
            return await propiska_page(request)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)

@router.get("/korpuss", response_class=HTMLResponse)
async def get_korpuss_page(request: Request):
    return templates.TemplateResponse("korpuss.html", {"request": request})

@router.get("/rooms", response_class=HTMLResponse)
async def get_rooms_page(request: Request):
    return templates.TemplateResponse("rooms.html", {"request": request})

# Опционально: маршрут для проверки доступных маршрутов
@router.get("/routes")
async def get_routes():
    return {"routes": [route.path for route in router.routes]}
