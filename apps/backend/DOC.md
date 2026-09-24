Для основных зависимостей (production/backend):
uv export --no-dev --no-hashes -o requirements.txt

Или если ему нужны и dev-инструменты (ruff, ty):
uv export --all-groups --no-hashes -o requirements-dev.txt
## Для разработчика на pip

### 1. Установка зависимостей
```bash
# Активировать своё venv, затем:
pip install -r requirements.txt       # только проект
pip install -r requirements-dev.txt   # проект + ruff + ty

### 2. Использование Ruff (Линтер и форматтер)

# Проверить код на ошибки стиля и логики
ruff check .

# Автоматически исправить простые ошибки и отсортировать импорты
ruff check --fix .
# Отформатировать весь код проекта
ruff format .

### 3. Использование ty (Проверка типов от Astral)

# Проверить типы во всём проекте
ty check

│ Примечание: Если команды ruff или ty не находятся напрямую в терминале, запускай их
│ через модуль Python в активном venv:
│ python -m ruff check .
│ python -m ty check
