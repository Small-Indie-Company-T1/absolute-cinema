# absolute-cinema
Основы веб-разработки на Python

1) Установка окружения и зависимостей


Сначала установите uv, если он еще не установлен. Затем выполните команду в корне проекта:

```shell
uv sync
```

Эта команда создаст виртуальное окружение (например, `.venv`) и установит зависимости, зафиксированные в `uv.lock`.

2) Запуск локального сервера

Запускайте команды внутри виртуального окружения через `uv run`:

```shell
uv run python manage.py runserver
```

3) Миграции

```shell
uv run python manage.py migrate
```

Создайте миграции для изменений в моделях (при необходимости):

```shell
uv run python manage.py makemigrations
uv run python manage.py migrate
```

4) Создание суперпользователя (админка)

```shell
uv run python manage.py createsuperuser
```

5) Добавление новой зависимости

Используйте `uv add`, чтобы корректно обновить `pyproject.toml` и `uv.lock`:

```shell
uv add requests
```

После добавления не забудьте закоммитить изменения в `pyproject.toml` и `uv.lock`.

