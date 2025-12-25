# AGENTS.md

Інструкції для AI-агентів при роботі з Python проєктами.

## Менеджер пакетів

Завжди використовуй **uv** для всіх операцій з пакетами:

```bash
# Створення проєкту
uv init my-project

# Додавання залежностей
uv add requests pytest

# Додавання dev-залежностей
uv add --dev mypy ruff

# Встановлення залежностей
uv sync

# Запуск скриптів
uv run python main.py
uv run pytest
```

## Версіонування

Використовуй **semantic versioning** (MAJOR.MINOR.PATCH):

- **MAJOR** — несумісні зміни API (1.0.0 → 2.0.0)
- **MINOR** — нова функціональність, сумісна зі старою (1.0.0 → 1.1.0)
- **PATCH** — виправлення помилок (1.0.0 → 1.0.1)

```toml
# pyproject.toml
[project]
version = "1.2.3"
```

## Linting та Formatting

Використовуй **ruff** для перевірки коду та форматування:

```bash
# Перевірка коду (linting)
uv run ruff check .

# Автоматичне виправлення проблем
uv run ruff check --fix .

# Форматування коду
uv run ruff format .

# Перевірка та форматування разом
uv run ruff check --fix . && uv run ruff format .
```

## Тестування

Використовуй **pytest**:

```bash
# Запуск тестів
uv run pytest

# З покриттям коду
uv run pytest --cov=axe_core_python --cov-report=html

# Конкретний тест
uv run pytest tests/test_axe_selenium.py::test_function

# Запуск з виводом print
uv run pytest -s
```
