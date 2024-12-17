# your_application/app.py
import os

def serve_static_file(path):
    """Чтение статических файлов (CSS, JS, изображения)"""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None  # Вернем None, если файл не найден

def get_html_file(path):
    """Получение HTML-контента по маршруту"""
    html_files = {
        '/register': 'registration.html',
        '/korpus': 'korpus.html',
        '/propiska': 'propiska.html',
        '/wrongemail': 'wrongemail.html',
        '/rooms': 'rooms.html',
        '/success': 'success.html',
    }
    return html_files.get(path)
