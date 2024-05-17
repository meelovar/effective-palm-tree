Запуск проверялся с `docker-ce` версии 26.1 и Python 3.12.

# Запуск

Скопировать `dotenv_example` как `.env`.

```shell
docker compose build
docker compose up -d
```

Сервер будет доступен по адресу `localhost:8000`

По умолчанию вместо отправки email выдаются в консоль. Их можно увидеть в логах
`dramatiq`. Чтобы настроить отправку email нужно закомментировать строку 135 в
в файле [src/project/settings.py](src/project/settings.py). И прописать верные
настройки в файле `.env`. Проверялось с SMTP сервером Яндекса.
