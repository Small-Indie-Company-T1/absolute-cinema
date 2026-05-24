# absolute cinema

## О проекте


- Django + Django REST Framework
- Flask
- FastAPI

Каждый сервис отвечает за отдельную часть продукта и демонстрирует разные подходы к построению backend-архитектуры.

Absolute Cinema — это backend-платформа для онлайн-кинотеатра.

### Реализованные возможности

- каталог фильмов
- подписки пользователей
- взаимодействия пользователей с контентом
- пользовательский контент (UGC)
- отдельный FastAPI-сервис
- REST API
- сервисный слой
- валидация и обработка ошибок
- модульная архитектура

### Практические темы, затронутые в проекте

- Django
- Flask
- FastAPI
- DRF
- сервисная архитектура
- асинхронность
- взаимодействие сервисов
- построение production-ready backend-приложений

## Стек технологий

### Основной стек

- Python 3.12+
- Django
- Django REST Framework
- Flask
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- uv

## Структура репозитория
<pre>
absolute-cinema-develop/
├── django_project/                  
│   ├── catalog/                    
│   │   ├── api/                     
│   │   ├── domain/                  
│   │   ├── migrations/              
│   │   ├── services/                
│   │   └── tests/                   
│   │
│   ├── config/                      
│   │   ├── components/              
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── core/                       
│   ├── interactions/              
│   ├── subscriptions/               
│   ├── users/                       
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── pyproject.toml
│
├── fastapi_service/                
│   ├── app/
│   │   ├── api/v1/                  
│   │   ├── core/                    
│   │   ├── schemas/                
│   │   └── services/                
│   │
│   ├── tests/
│   ├── main.py
│   └── pyproject.toml
│
├── flask_service/                   
│   ├── app/
│   │   ├── api/                     
│   │   ├── errors/                  
│   │   ├── models/                  
│   │   ├── repositories/            
│   │   ├── schemas/                 
│   │   ├── services/                
│   │   ├── config.py
│   │   └── extensions.py
│   │
│   ├── migrations/                  
│   ├── main.py
│   ├── run.py
│   └── pyproject.toml
│
└── README.md
</pre>



### Распределение ответственности сервисов

| Сервис | Ответственность |
|--------|-----------------|
| Django | Основной бизнес-домен и REST API |
| Flask | Пользовательский контент (UGC) |
| FastAPI | Отдельный современный async-сервис |

### Слои внутри сервисов

- API layer
- Services layer
- Domain layer
- Repository layer
- Schemas / DTO

### Преимущества такого подхода

- отделение HTTP от бизнес-логики
- простота тестирования кода
- масштабируемость проекта
- переиспользование бизнес-логики
- избежание fat-controller архитектуры

## Тематика проекта

Проект выполнен в тематике онлайн-кинотеатра.

### Основные сущности

- Movie
- Genre
- Subscription
- Watchlist
- User
- Review / Comment / Rating

### Возможности пользователя

- просматривать каталог фильмов
- получать детальную информацию
- добавлять фильмы в список
- оставлять пользовательский контент
- взаимодействовать с защищёнными endpoint-ами

## Основные особенности

### Django 

Реализовано:

- модели и миграции
- Django ORM
- Django Admin
- REST API
- serializers
- viewsets и routers
- фильтрация и пагинация
- сервисный слой
- единый формат ошибок

### Flask сервис

Flask используется как лёгкий backend для пользовательского контента.

Реализовано:

- CRUD для UGC
- валидация пользовательского ввода
- статусы модерации
- интеграция с Django API
- сервисный слой и repositories

### FastAPI сервис

FastAPI используется как production-ready async backend.

Реализовано:

- async endpoints
- Pydantic schemas
- OpenAPI документация
- background tasks
- JWT авторизация
- взаимодействие между сервисами

## Взаимодействие сервисов

Проект демонстрирует базовую микросервисную архитектуру.

### Сценарий взаимодействия

- Django выступает основным backend-приложением
- Flask сервис обрабатывает пользовательский контент
- FastAPI сервис выполняет отдельные async-задачи
- Сервисы взаимодействуют между собой через HTTP API

### Примеры

- Flask проверяет существование фильма через Django API
- Django может вызывать FastAPI сервис
- FastAPI выполняет фоновые задачи

## Технические особенности

### Service Layer

Бизнес-логика вынесена из controllers/views в отдельные сервисы.

Преимущества:

- отсутствие дублирования кода
- централизация правил
- упрощение поддержки

### Domain-driven подход

В проекте разделены:

- HTTP-слой
- бизнес-логика
- модели данных
- работа с БД

### Валидация

Используются:

- DRF Serializers
- Pydantic
- схемы Flask

### Обработка ошибок

Реализованы:

- доменные исключения
- единый формат ошибок
- HTTP mapping


## Инструкция по запуску

### 1. Клонирование репозитория

```bash
git clone <repo_url>
cd absolute-cinema

## Запуск

1. Установить uv
2. Установить зависимости
```bash
uv sync
```
3. Создать `.env` по образцу `.env.example`
4. Запустить сервис
```bash
uv run python run.py
```
