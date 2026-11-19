# Docker

## Установка

```bash
# официальный скрипт (Debian/Ubuntu/Fedora и др.)
curl -fsSL https://get.docker.com | sudo sh

# запуск без sudo
sudo usermod -aG docker $USER
newgrp docker          # или перелогиниться

docker --version
docker run hello-world
```

> Официальный скрипт ставит Docker из репозитория Docker, а не из репозитория дистрибутива.
> На учебной машине лучше согласовать это с преподавателем.

## Основные команды

```bash
docker ps                  # запущенные контейнеры
docker ps -a               # все, включая остановленные
docker images              # образы
docker pull ubuntu:24.04   # скачать образ
docker run -it ubuntu bash # запустить контейнер и войти внутрь (выход: exit)
docker run -d -p 8080:80 nginx     # в фоне, порт 8080 → 80
docker logs -f имя         # логи в реальном времени
docker exec -it имя bash   # войти в работающий контейнер
docker stop имя            # остановить
docker rm имя              # удалить контейнер
docker rmi образ           # удалить образ
```

`--rm` удаляет контейнер сразу после завершения:

```bash
docker run --rm python:3.12 python -c "print('привет')"
```

## Частые сценарии

```bash
# python-скрипт из текущей папки
docker run --rm -v "$PWD":/app -w /app python:3.12 python main.py

# mysql для лабораторной
docker run -d --name db -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:8

# postgres
docker run -d --name pg -e POSTGRES_PASSWORD=root -p 5432:5432 postgres:16
```

`-v "$PWD":/app` — пробрасывает папку с кодом внутрь контейнера. Без этого изменения не сохранятся.

## Docker Compose

Файл `compose.yaml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./site:/usr/share/nginx/html:ro

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: root
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d        # запустить всё
docker compose ps
docker compose logs -f
docker compose down         # остановить и удалить
docker compose down -v      # вместе с данными
```

## Сборка своего образа

`Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
docker build -t моя-лаба .
docker run --rm моя-лаба
```

## Уборка

```bash
docker system df              # сколько занимает
docker container prune        # удалить остановленные
docker image prune             # удалить неиспользуемые образы
docker system prune -a         # всё неиспользуемое (осторожно)
```

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `permission denied while trying to connect to the Docker daemon` | нет прав | `sudo usermod -aG docker $USER` + перелогин |
| `port is already allocated` | порт занят | взять другой: `-p 8081:80` |
| `Cannot connect to the Docker daemon` | служба не запущена | `sudo systemctl start docker` |
| `command not found: docker` | не установлен | команда установки выше |
| изменения в коде не видны | забыли `-v` | пробросить папку через `-v` |
| контейнер сразу завершается | процесс закончился | смотреть `docker logs имя` |
