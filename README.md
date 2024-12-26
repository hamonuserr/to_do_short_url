## Final project

## How to start👻

Клонируем проект: 
```bash
git clone git@github.com:Denmais/FastAPI_API.git

```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```

```bash
Linux: source venv/bin/activate
```

И установить зависимости из файла requirements.txt (в обоих папках):
```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Далее необходимо собрать образы бэкенда (из любой папки).
```bash
docker build -t username/backend .
```

Запустить контейнер
```bash
docker run -d -p 8000:80 -v todo_data:/app/data username/backend:latest
```

## 2. Команды для запуска 2<a id=2></a>

Выполнить команды в терминале:
```bash
docker run -d -p 8000:80 -v todo_data:/app/data denmais/todo-service:latest
```
или (можно поменять порты)

```bash
docker run -d -p 8000:80 -v shorturl_data:/app/data denmais/shorturl-service
```

