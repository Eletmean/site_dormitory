import os

def serve_static_file(file_path):
    """Возвращает содержимое статического файла, если он существует."""
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    return None

def get_html_file(path):
    """Возвращает имя HTML-файла на основе пути."""
    if path == '/register':
        return 'registration.html'  # Например, главная страница
    elif path == '/korpus':
        return 'korpus.html'
    elif path == '/propiska':
        return 'propiska.html'
    elif path == '/wrongemail':
        return 'wrongemail.html'
    elif path == '/rooms':
        return 'rooms.html'
    elif path == '/success':
        return 'success.html'
    else:
        return None  # Если файл не найден
