## Final project

## How to start👻

Клонируем проект: 
```bash
git clone git@github.com:hamonuserr/to_do_short_url.git
```

Создаем и активируем виртуальное окружение:
```bash
python -m venv venv
```

Устанавливаем зависимости из обеих папок:
```bash
pip install -r requirements.txt
```

Собираем образы:
```bash
docker build -t hamonuserr/backend .
```

Запускаем контейнер:
```bash
docker run -d -p 8000:80 -v todo_data:/app/data username/backend:latest
```

## Команды для запуска 2<a id=2></a>

Выполнить команды в терминале:
```bash
docker run -d -p 8000:80 -v todo_data:/app/data hamonuserr/todo-service:latest
```


```bash
docker run -d -p 8000:80 -v shorturl_data:/app/data hamonuserr/shorturl-service
```

