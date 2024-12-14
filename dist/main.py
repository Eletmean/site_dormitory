from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
import os
import bcrypt

# Настройка базы данных
DATABASE_URL = "mysql+pymysql://root:123@127.0.0.1/user_database"  # Замените на ваши данные
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))  # Храните хэшированный пароль

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Определение схемы для регистрации пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str

app = FastAPI()

# Настройка для раздачи статических файлов из папки src
app.mount("/static", StaticFiles(directory="src"), name="static")

# Функция для чтения HTML файлов с обработкой ошибок
def read_html_file(file_name: str) -> str:
    try:
        file_path = os.path.join("src", file_name)
        with open(file_path, encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"<h1>Ошибка 404: Файл {file_name} не найден.</h1>"
    except Exception as e:
        return f"<h1>Ошибка: {str(e)}</h1>"

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршруты для HTML страниц
@app.get("/", response_class=HTMLResponse)
async def read_index():
    return read_html_file("index.html")

@app.get("/rooms", response_class=HTMLResponse)
async def read_rooms():
    return read_html_file("rooms.html")

@app.get("/korpuss", response_class=HTMLResponse)
async def read_korpuss():
    return read_html_file("korpuss.html")

@app.post("/submit-booking", response_class=HTMLResponse)
async def submit_booking():
    return read_html_file("success.html")

# Эндпоинт для регистрации пользователя
@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существования пользователя с таким email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    # Хэширование пароля
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Создание нового пользователя
    new_user = User(email=user.email, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован", "user_id": new_user.id}

