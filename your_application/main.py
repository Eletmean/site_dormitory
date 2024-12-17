# your_application/main.py
from fastapi import FastAPI
from .app import app as api_app
from .database import init_db

app = FastAPI()

# Инициализация базы данных
init_db()

# Подключаем маршруты
app.include_router(api_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
