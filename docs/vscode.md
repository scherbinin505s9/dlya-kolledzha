# VS Code

## Установка

```bash
# Debian / Ubuntu: скачать .deb с code.visualstudio.com и установить
sudo apt install -y ./code_*.deb

# Arch
sudo pacman -S code

# Fedora
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install -y code
```

Запуск из терминала:

```bash
code .            # открыть текущую папку
code файл.py      # открыть файл
code --new-window .
```

Если `code: command not found` — в VS Code: `Ctrl+Shift+P` → **Shell Command: Install 'code' command in PATH**.

## Полезные расширения

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension eamodio.gitlens
code --install-extension usernamehw.errorlens
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-vscode-remote.remote-ssh
```

| Расширение | Зачем |
|---|---|
| Python + Pylance | подсказки, отладка, окружения |
| ESLint + Prettier | проверка и автоформатирование JS/TS |
| GitLens | история строк, авторство |
| Error Lens | ошибка показывается прямо в строке |
| Docker | контейнеры в боковой панели |
| Remote - SSH | работа на удалённой машине как локально |

## Настройки

`Ctrl+Shift+P` → **Preferences: Open User Settings (JSON)**:

```json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "terminal.integrated.defaultProfile.linux": "bash",
  "python.defaultInterpreterPath": ".venv/bin/python",
  "explorer.confirmDelete": false
}
```

Для Python удобнее `"editor.tabSize": 4`.

## Python в VS Code

1. Открыть папку проекта (`code .`).
2. `Ctrl+Shift+P` → **Python: Select Interpreter** → выбрать `.venv/bin/python`.
3. Слева внизу должен быть виден `(.venv)`.
4. Запуск: `F5` (с отладкой) или кнопка ▶.

Если не видит окружение — проверить, что `.venv` создан **внутри** папки проекта.

## Работа с удалённой машиной

`Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → `user@192.168.0.10`.

Дальше всё как локально: терминал, файлы, расширения. Код выполняется на удалённой машине, поэтому Python/Docker должны быть установлены **там**.

Для этого нужен SSH-доступ:

```bash
ssh user@192.168.0.10
```

## Горячие клавиши

| Клавиши | Действие |
|---|---|
| `Ctrl+P` | быстрое открытие файла |
| `Ctrl+Shift+P` | палитра команд |
| `Ctrl+`` ` | терминал |
| `Ctrl+/` | закомментировать строку |
| `Alt+↑ / ↓` | переместить строку |
| `Shift+Alt+↓` | дублировать строку |
| `Ctrl+D` | выделить следующее такое же слово |
| `Ctrl+Shift+F` | поиск по проекту |
| `F2` | переименовать символ во всём проекте |
| `Ctrl+K Z` | режим дзен (выход: Esc Esc) |

## Настройки в git

Папку `.vscode/` обычно коммитят, чтобы у всей группы были одинаковые настройки, но личные `settings.json` — нет.

`.gitignore`:

```
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
```
