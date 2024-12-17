from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Настройка конфигурации приложения (например, секретный ключ)
    app.config['SECRET_KEY'] = '123'

    # Импорт маршрутов
    from .routes import main
    app.register_blueprint(main)

    return app