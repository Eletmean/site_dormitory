# your_application/wsgi.py
from wsgiref.simple_server import make_server
from your_application.routes import router  # Импортируйте ваш router

# Определите объект application
application = router  # Это должен быть ваш WSGI-приложение

if __name__ == "__main__":
    httpd = make_server('', 8000, application)  # Используйте application здесь
    print("Serving on port 8000...")
    httpd.serve_forever()
