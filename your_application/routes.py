import os
from your_application.app import serve_static_file, get_html_file

def router(environ, start_response):
    # Получаем запрашиваемый путь
    path = environ.get('PATH_INFO', '/')

    # Обработка статических файлов (CSS, JS, изображения)
    if path.startswith('/styles/') or path.startswith('/js/') or path.startswith('/images/'):
        static_file_path = os.path.join('src', path[1:])  # Убираем начальный слэш и добавляем путь к src
        file_content = serve_static_file(static_file_path)

        if file_content is None:
            start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
            return [b'404 Not Found']

        # Определение типа контента
        if path.startswith('/styles/'):
            content_type = 'text/css'
        elif path.startswith('/js/'):
            content_type = 'application/javascript'
        elif path.startswith('/images/'):
            content_type = 'image/jpeg' if path.endswith('.jpg') else 'image/png' if path.endswith('.png') else 'image/gif'
        else:
            content_type = 'application/octet-stream'

        start_response('200 OK', [('Content-type', content_type)])
        return [file_content]

    # Обработка HTML-файлов для заданных маршрутов
    html_files = {
        '/register': 'registration.html',
        '/rooms': 'rooms.html',
        '/success': 'success.html',
        '/wrongemail': 'wrongemail.html',
        '/propiska': 'propiska.html'
    }

    # Получаем имя HTML-файла по маршруту
    html_file = html_files.get(path)
    if html_file:
        file_path = os.path.join('src', html_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
            return [html_content.encode('utf-8')]
        except FileNotFoundError:
            start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
            return [b'404 Not Found']

    # Если ни один маршрут не сработал, возвращаем 404
    start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8')])
    return [b'404 Not Found']
