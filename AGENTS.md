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
# Запуск швидких тестів (unit тести, без браузерів)
uv run pytest

# Запуск усіх тестів включаючи повільні браузерні
uv run pytest --runslow

# Запуск тестів для конкретного браузера
uv run pytest --runslow -m chromium
uv run pytest --runslow -m firefox
uv run pytest --runslow -m webkit

# Запуск тестів за типом
uv run pytest -m unit          # Швидкі unit тести
uv run pytest --runslow -m selenium    # Selenium тести
uv run pytest --runslow -m playwright  # Playwright тести

# З покриттям коду
uv run pytest --cov=axe_core_python --cov-report=html

# Конкретний тест
uv run pytest tests/test_axe_selenium.py::TestSeleniumFirefox::test_run_axe_basic

# Запуск з виводом print
uv run pytest -s
```

### Маркери тестів

Тести організовані за маркерами:

- `unit` — швидкі unit тести без браузерів
- `slow` — повільні тести (вимагають `--runslow`)
- `selenium` — тести з Selenium WebDriver
- `playwright` — тести з Playwright
- `chrome`, `firefox`, `chromium`, `webkit` — тести для конкретних браузерів

### Структура тестів

```
tests/
├── conftest.py          # Fixtures та pytest hooks
├── test_base.py         # Unit тести для базових класів
├── test_axe_selenium.py # Selenium integration тести
├── test_axe_sync_playwright.py   # Sync Playwright тести
├── test_axe_async_playwright.py  # Async Playwright тести
└── test_page.html       # HTML сторінка для тестування
```
