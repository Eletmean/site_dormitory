import os
from wsgiref.simple_server import make_server

def serve_static_file(path):
    """Чтение статических файлов (CSS и JS)"""
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None  # Вернем None, если файл не найден

def simple_app(environ, start_response):
    # Получаем путь запроса
    path = environ.get('PATH_INFO', '/')

    # Определяем путь к HTML-файлам
    html_files = {
        '/register': 'registration.html',
        '/korpus': 'korpus.html',
        '/propiska': 'propiska.html',
        '/wrongemail': 'wrongemail.html',
        '/rooms': 'rooms.html',
         '/success': 'success.html',
    }

    # Обработка статических файлов
    if path.startswith('/styles/') or path.startswith('/js/'):
        static_file_path = os.path.join('src', path[1:])  # Убираем начальный слэш и добавляем путь к src
        file_content = serve_static_file(static_file_path)
        if file_content is None:
            start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
            return []  # Пустой ответ для 404

        # Определяем тип контента
        content_type = 'text/css' if path.endswith('.css') else 'application/javascript'
        start_response('200 OK', [('Content-type', content_type)])
        return [file_content]

    # Обработка HTML-файлов
    if path in html_files:
        file_path = os.path.join('src', html_files[path])
    else:
        # Если запрашиваемая страница не найдена
        start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
        return []  # Пустой ответ для 404

    # Чтение содержимого HTML-файла
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
        return []  # Пустой ответ для 404

    # Возвращаем HTML-контент
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    return [html_content.encode('utf-8')]

# Запуск WSGI сервера
httpd = make_server('', 8000, simple_app)
print("Serving on port 8000...")
httpd.serve_forever()
