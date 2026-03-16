# Wallet API

Асинхронный REST API для работы с балансом кошельков на FastAPI, SQLAlchemy и PostgreSQL.

## Возможности

- Получение баланса кошелька
- Пополнение и списание средств
- Блокировка строки кошелька при изменении баланса (`SELECT ... FOR UPDATE`) для корректной работы при конкурентных
  запросах

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- PostgreSQL 16
- Alembic
- Pytest
- Docker / Docker Compose

## Структура проекта

```text
app/
  api/            # роуты API
  db/             # настройка движка и сессий БД
  models/         # модели SQLAlchemy
  schemas/        # схемы Pydantic
alembic/          # миграции
tests/            # тесты
```

## Переменная окружения

- `DATABASE_URL` в формате:
  `postgresql+asyncpg://postgres:postgres@db:5432/wallets`

## Быстрый старт (Docker)

1. Поднимите сервисы:

```bash
docker compose up -d --build
```

2. Примените миграции:

```bash
docker compose exec api alembic upgrade head
```

3. Проверьте health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Ожидаемый ответ:

```json
{
  "status": "ok"
}
```

## API

Базовый префикс: `/api/v1`

### `GET /health`

Проверка доступности сервиса.

### `GET /wallets/{WALLET_UUID}`

Получение баланса кошелька.

Успешный ответ:

```json
{
  "balance": 1000
}
```

### `POST /wallets/{WALLET_UUID}/operation`

Изменение баланса кошелька.

Тело запроса:

```json
{
  "operation_type": "DEPOSIT",
  "amount": 500
}
```

Где:

- `operation_type`: `DEPOSIT` или `WITHDRAW`
- `amount`: целое число больше 0

Успешный ответ:

```json
{
  "balance": 1500
}
```

Типовые ошибки:

- `404 Wallet not found`
- `400 Wallet balance too low`

## Тесты

```bash
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm api python -m pytest -q
```

Примечание: перед первым запуском убедитесь, что тестовая БД существует и к ней применены миграции.
