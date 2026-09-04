# Location Popularity Map API

REST API для каталогу цікавих локацій з відгуками, рейтингами, голосами та автоматичною популярністю.

Проєкт побудований на Django REST Framework і використовує PostgreSQL як основну базу даних та Redis для кешування і контролю переглядів.

## Що реалізовано

- Session + Cookie authentication через стандартний Django auth
- реєстрація, login, logout і password reset
- CRUD категорій
- CRUD локацій із soft delete
- права автора та адміністратора
- відгуки з рейтингом від 1 до 5
- один відгук користувача на локацію
- Like/Dislike відгуків із можливістю зміни голосу
- автоматичний рейтинг і popularity через Django ORM
- обмеження переглядів: один користувач і локація раз на годину
- пошук, фільтрація, сортування та пагінація
- Redis-кеш списку локацій
- JSON і CSV export
- Docker Compose для Django, PostgreSQL і Redis
- базові API smoke-тести

## Стек

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL 17
- Redis 8
- django-filter
- pandas
- pytest
- Docker Compose

## Швидкий старт через Docker

Переконайтеся, що Docker Desktop запущений.

```powershell
docker compose up -d --build
docker compose exec web python manage.py migrate
```

API буде доступний за адресою:

```text
http://localhost:8000/
```

Перевірка стану:

```text
GET http://localhost:8000/health/
```

Зупинка сервісів:

```powershell
docker compose down
```

Щоб видалити також дані PostgreSQL і Redis:

```powershell
docker compose down -v
```

## Локальний запуск через .venv

Створіть або активуйте віртуальне середовище та встановіть залежності:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Створіть локальний `.env` на основі `.env.example`. Файл `.env` не додається до Git.

Для локального запуску потрібні PostgreSQL і Redis на стандартних портах `5432` і `6379`.

```powershell
python manage.py migrate
python manage.py runserver
```

## Основні endpoint-и

### Системні

```text
GET  /
GET  /health/
GET  /admin/
```

### Authentication

```text
POST /auth/register/
POST /auth/login/
POST /auth/logout/
POST /auth/password-reset/
POST /auth/password-reset/confirm/<uidb64>/<token>/
```

Auth працює через сесію та cookie. Для browser-based unsafe requests Django CSRF protection залишається увімкненим.

### Categories

```text
GET    /api/categories/
POST   /api/categories/
GET    /api/categories/<id>/
PUT    /api/categories/<id>/
PATCH  /api/categories/<id>/
DELETE /api/categories/<id>/
```

Перегляд доступний усім. Зміни доступні авторизованим користувачам.

### Locations

```text
GET    /api/locations/
POST   /api/locations/
GET    /api/locations/<id>/
PUT    /api/locations/<id>/
PATCH  /api/locations/<id>/
DELETE /api/locations/<id>/
```

Створення доступне авторизованим користувачам. Редагування та soft delete доступні автору локації або адміністратору.

Приклади параметрів списку:

```text
/api/locations/?search=park
/api/locations/?category=1&author=2
/api/locations/?rating=4
/api/locations/?ordering=-created_at
/api/locations/?ordering=-average_rating
/api/locations/?ordering=-popularity_score
/api/locations/?page=2&page_size=50
```

### Reviews and votes

```text
GET    /api/reviews/
POST   /api/reviews/
GET    /api/reviews/<id>/
PATCH  /api/reviews/<id>/
DELETE /api/reviews/<id>/
POST   /api/reviews/<id>/vote/
```

Тіло vote-запиту:

```json
{"vote_type": "like"}
```

Допустимі значення: `like` або `dislike`.

### Export

```text
GET /api/locations/export/json/
GET /api/locations/export/csv/
```

Export підтримує ті самі query-параметри пошуку, фільтрації та сортування, що й список локацій.

## Popularity

Похідні значення не зберігаються в базі даних. Вони обчислюються ORM annotations під час запиту.

Поточна формула:

```text
popularity = rating_score * 0.50
           + review_score * 0.30
           + recent_view_score * 0.20
```

Нормалізація:

- рейтинг: середній рейтинг від `0` до `5`
- відгуки: максимум `10` відгуків у нормалізованому score
- перегляди: максимум `20` переглядів за останні `7` днів

## Перевірки

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe -m mypy locations reviews config
.\.venv\Scripts\python.exe -m pytest -q
```

Поточний базовий набір містить smoke-тести health, списку/створення локації та створення відгуку.

## Структура

```text
config/       Django settings, URL routing, auth API, health API
locations/    Category, Location, views, filters, cache, exports
reviews/      Review, ReviewVote, serializers, permissions, API
templates/    password reset email templates
Dockerfile
docker-compose.yml
requirements.txt
```

## Відкладені бонуси

У межах мінімального обов'язкового scope не реалізовані:

- email-повідомлення автору локації після нового відгуку
- підписка на оновлення конкретної локації
- email-сповіщення підписникам про нові відгуки

На їх реалізацію за нашим workflow варто закласти приблизно 2–4 години: окремі моделі підписок, email-сервіс, тести, налаштування delivery та фінальна перевірка. Це можна зробити після стабілізації основного API, не змінюючи базову модель локацій і відгуків.
