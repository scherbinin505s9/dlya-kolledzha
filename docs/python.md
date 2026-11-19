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

## Tkinter и PyQt

По «Основам алгоритмизации» GUI делают на Python. Tkinter уже входит в Python,
PyQt ставится отдельно.

### Tkinter: минимум для лабораторной

```python
import tkinter as tk
from tkinter import messagebox


def calculate():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return
    result.config(text=f"Сумма: {a + b}")


root = tk.Tk()
root.title("Калькулятор")
root.geometry("320x200")

tk.Label(root, text="Первое число").pack()
entry_a = tk.Entry(root)
entry_a.pack()

tk.Label(root, text="Второе число").pack()
entry_b = tk.Entry(root)
entry_b.pack()

tk.Button(root, text="Сложить", command=calculate).pack(pady=8)
result = tk.Label(root, text="Сумма: —")
result.pack()

root.mainloop()
```

Что проверяют: окно запускается, поля ввода работают, кнопка считает,
нечисловой ввод не роняет программу, результат обновляется.

### PyQt6

```bash
source .venv/bin/activate
pip install PyQt6
```

```python
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def on_click():
    label.setText("Привет!")


app = QApplication([])
window = QWidget()
window.setWindowTitle("PyQt")

layout = QVBoxLayout()
label = QLabel("Нажми кнопку")
button = QPushButton("Нажать")
button.clicked.connect(on_click)
layout.addWidget(label)
layout.addWidget(button)
window.setLayout(layout)
window.show()

app.exec()
```

| Что | Tkinter | PyQt6 |
|---|---|---|
| Установка | встроен | `pip install PyQt6` |
| Простота | проще | больше возможностей |
| Вид | стандартный | нативный |
| Для лабы | обычно достаточно | если требует методичка |

### Частые ошибки GUI

| Ошибка | Причина | Решение |
|---|---|---|
| `no display name` в WSL | нет графической среды | запускать из Windows или настроить X-сервер |
| Окно не появляется | забыт `mainloop()` / `app.exec()` | добавить в конец |
| Кнопка не реагирует | обработчик не привязан | `command=` в Tkinter, `clicked.connect` в PyQt |
| `ValueError` при вводе | `float("abc")` | обернуть в `try/except` и показать сообщение |

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `externally-managed-environment` | попытка `pip install` в систему | создать `venv` |
| `ModuleNotFoundError` | пакет стоит в другом окружении | активировать `.venv`, проверить `which python3` |
| `command not found: python` | в Linux команда называется `python3` | использовать `python3` |
| `No module named venv` | не установлен `python3-venv` | `sudo apt install python3-venv` |
| `IndentationError` | смешаны табы и пробелы | в редакторе включить «пробелы, 4» |
| `SyntaxError` после копирования | в коде символы из Word (`“ ” —`) | печатать кавычки вручную |
