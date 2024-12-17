from wsgiref.simple_server import make_server
from your_application.routes import simple_app  # Убедитесь, что здесь simple_app

if __name__ == "__main__":
    httpd = make_server('', 8000, simple_app)
    print("Serving on port 8000...")
    httpd.serve_forever()