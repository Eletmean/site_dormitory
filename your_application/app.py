from fastapi import FastAPI
from your_application.routes import router  # Импортируйте маршруты

app = FastAPI()

# Регистрация маршрутов
app.include_router(router)