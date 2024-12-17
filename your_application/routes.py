from your_application import app  # Импортируем экземпляр приложения

@app.route('/')  # Определяем маршрут для главной страницы
def hello():
    return "Hello, World!"  # Возвращаем строку