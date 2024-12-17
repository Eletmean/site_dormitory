# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY dist/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY dist/ .

# Открываем порт, который будет использоваться приложением
EXPOSE 8000

# Команда для запуска вашего приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]