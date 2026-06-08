# DRF проект с Docker, PostgreSQL, Redis и Celery

Этот проект представляет собой взаимодействие по API через DRF, которое полностью запускается в контейнерах Docker. Включает
PostgreSQL как основную базу данных, Redis как брокер сообщений, Celery для фоновых задач и Celery Beat
для периодических задач.

# Документация методов
Ознакомитсья с документацией методов можно по [ссылке](http://localhost:8000/docs/).  
Далее будут описаны действия для начала работы с проектом.

## Требования

Перед началом убедитесь, что на вашем компьютере установлены:

- **Docker Desktop** (версия 4.20 или выше)
    - [Скачать для Windows/Mac](https://www.docker.com/products/docker-desktop/)
- **Git** (опционально, для клонирования репозитория)
- **Poetry** (опционально, для локальной разработки без Docker)

## Быстрый старт

### 1. Клонировать репозиторий

```git clone <url-репозитория>```

```cd drf_first_project```

### 2. Настроить переменные окружения

Скопируйте файл .env.template в .env, отредактируйте .env, установив свои значения

### 3. Запустить проект

```docker-compose up --build```

После успешного запуска вы увидите логи контейнеров. Django будет доступен по адресу:  
http://localhost:8000/

### 4. Создать суперпользователя (админку)

```docker-compose exec project python manage.py createsuperuser```

Теперь вы можете зайти в админ-панель:
http://localhost:8000/admin

## Управление проектом

| Действие                           | Команда                                                       |
|------------------------------------|---------------------------------------------------------------|
| Запустить все сервисы              | `docker-compose up`                                           |
| Запустить в фоне                   | `docker-compose up -d`                                        |
| Остановить все сервисы             | `docker-compose down`                                         |
| Остановить и удалить тома (данные) | `docker-compose down -v`                                      |
| Пересобрать образы                 | `docker-compose build --no-cache`                             |
| Посмотреть логи                    | `docker-compose logs -f`                                      |
| Выполнить миграции БД              | `docker-compose exec project python manage.py migrate`        |
| Создать миграции                   | `docker-compose exec project python manage.py makemigrations` |
| Зайти в оболочку Django            | `docker-compose exec project python manage.py shell`          |
| Зайти в базу данных                | `docker-compose exec db psql -U myuser -d mydatabase`         |

## Структура сервисов

Проект состоит из 5 контейнеров:

| Сервис        | Описание                                      | Доступность с хоста |
|---------------|-----------------------------------------------|---------------------|
| `project`     | Django приложение (runserver)                 | `localhost:8000`    |
| `db`          | PostgreSQL 15                                 | -                   |
| `redis`       | Redis 7 (брокер для Celery)                   | -                   |
| `celery`      | Celery worker (выполняет фоновые задачи)      | -                   |
| `celery_beat` | Celery Beat (планировщик периодических задач) | -                   |

## Локальная разработка без Docker, если это требуется

Если вы хотите разрабатывать без Docker, убедитесь, что у вас установлены:

- Python 3.12
- PostgreSQL 15
- Redis 7
- Poetry

```
# Установить зависимости
poetry install

# Активировать виртуальное окружение
poetry shell

# Применить миграции
python manage.py migrate

# Запустить сервер
python manage.py runserver

# В отдельном терминале запустить Celery
celery -A core worker -l INFO

# И Celery Beat (опционально)
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler