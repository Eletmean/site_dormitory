from wsgiref.simple_server import make_server
from your_application import router  # Импортируйте router из __init__.py

if __name__ == "__main__":
    httpd = make_server('', 8000, router)  # Используйте router здесь
    print("Serving on port 8000...")
    httpd.serve_forever()