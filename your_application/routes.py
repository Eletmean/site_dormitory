from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dist.database import SessionLocal  # Импортируйте вашу сессию базы данных
from dist.models import User  # Импортируйте вашу модель пользователя
from passlib.context import CryptContext  # Импортируйте CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="src")

# Инициализация хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    except Exception as e:
        db.rollback()  # Откат транзакции в случае ошибки
        raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")

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