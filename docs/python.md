# Python

## Проверка и установка

```bash
python3 -V
pip3 --version
```

```bash
sudo apt install -y python3 python3-pip python3-venv   # Debian / Ubuntu
sudo dnf install -y python3 python3-pip               # Fedora
sudo pacman -S python python-pip                     # Arch
```

## Виртуальное окружение (обязательно)

Ставить пакеты в систему через `pip` нельзя: Debian/Ubuntu блокируют это ошибкой `externally-managed-environment` (PEP 668). Для каждой лабораторной — своё окружение.

```bash
cd лаба
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
deactivate
```

- `.venv` — папка окружения, её не коммитят (добавьте в `.gitignore`).
- Приглашение терминала меняется на `(.venv)`, значит окружение активно.
- Выйти: `deactivate`. Удалить: `rm -rf .venv`.

## Зависимости

```bash
pip freeze > requirements.txt     # зафиксировать текущие версии
pip install -r requirements.txt   # воспроизвести на другом компьютере
pip list                          # что установлено
pip install numpy pandas matplotlib jupyter
pip install -U пакет              # обновить
pip uninstall пакет
```

## Jupyter

```bash
source .venv/bin/activate
pip install jupyter
jupyter notebook      # откроется в браузере
jupyter lab           # более удобный интерфейс
```

## Запуск скрипта

```bash
python3 main.py
python3 -i main.py    # после выполнения остаться в интерактивной оболочке
python3               # REPL, выход: exit() или Ctrl+D
```

Исполняемый файл:

```python
#!/usr/bin/env python3
print("привет")
```

```bash
chmod +x main.py
./main.py
```

## Структура учебного проекта

```
лаба/
├── .venv/              # окружение, не в git
├── main.py             # точка входа
├── requirements.txt
├── .gitignore
└── README.md           # что делает работа, как запустить
```

`.gitignore`:

```
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
```

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `externally-managed-environment` | попытка `pip install` в систему | создать `venv` |
| `ModuleNotFoundError` | пакет стоит в другом окружении | активировать `.venv`, проверить `which python3` |
| `command not found: python` | в Linux команда называется `python3` | использовать `python3` |
| `No module named venv` | не установлен `python3-venv` | `sudo apt install python3-venv` |
| `IndentationError` | смешаны табы и пробелы | в редакторе включить «пробелы, 4» |
| `SyntaxError` после копирования | в коде символы из Word (`“ ” —`) | печатать кавычки вручную |
