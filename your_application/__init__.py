from flask import Flask

app = Flask(__name__)

# Импортируем маршруты после создания экземпляра приложения
from your_application.routes import *  # Импортируем маршруты