# Установка Playwright MCP

Playwright MCP — локальный сервер, который даёт агенту инструменты браузера:
открыть страницу, прочитать её, кликнуть, заполнить форму, снять скриншот.

## 1. Проверить Node.js

```bash
node -v
npx --version
```

Нужен Node.js 20 или новее. Установка — в [SETUP.md](../../../../SETUP.md).

## 2. Добавить сервер в конфиг

Глобальный конфиг OpenCode:

- Linux и macOS: `~/.config/opencode/opencode.jsonc`
- Windows: `C:\Users\<пользователь>\.config\opencode\opencode.jsonc`

Добавьте в `mcp.servers` блок `playwright`.

### Windows

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": [
          "cmd.exe",
          "/c",
          "npx",
          "-y",
          "@playwright/mcp@latest",
          "--browser",
          "chrome",
          "--user-data-dir",
          "%LOCALAPPDATA%\\opencode-browser"
        ]
      }
    }
  }
}
```

`chrome` можно заменить на `msedge`, если Chrome не установлен.

### Linux и macOS

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": [
          "npx",
          "-y",
          "@playwright/mcp@latest",
          "--browser",
          "chrome",
          "--user-data-dir",
          "/home/ПОЛЬЗОВАТЕЛЬ/.local/share/opencode-browser"
        ]
      }
    }
  }
}
```

Путь замените на свой: `echo $HOME`.

### Через CLI

На macOS и Linux:

```bash
opencode mcp add playwright --global -- \
  npx -y @playwright/mcp@latest --browser chrome
```

В PowerShell аргументы после `--` может съесть сама оболочка. Если команда
ругается на `-y` или `--browser` — правьте JSON вручную, как выше.

## 3. Проверить подключение

```bash
opencode mcp list
```

Ожидается:

```
✓ playwright  connected
```

Конфиг перечитывается автоматически. Если список пуст — перезапустите
OpenCode или выполните `/reload` в TUI.

Первый запуск скачивает пакет `@playwright/mcp` через `npx`, это занимает
до минуты.

## 4. Первый запуск браузера

Попросите агента:

```
Открой https://example.com и покажи заголовок страницы
```

Откроется отдельное окно Chrome с профилем
`%LOCALAPPDATA%\opencode-browser` (Windows) или
`~/.local/share/opencode-browser` (Linux/macOS).

Это **не** ваш основной браузер: закладки и пароли из него не подхватываются.
Зато вход на сайты сохраняется между запусками.

## 5. Вход на сайты

1. Агент открывает страницу входа.
2. Вы вводите логин и пароль **сами** в открывшемся окне.
3. Дальше агент работает с сайтом уже авторизованным.

Пароль агенту сообщать не нужно и не следует.

## Удаление

1. Уберите блок `playwright` из `opencode.jsonc`.
2. Удалите папку профиля:
   - Windows: `%LOCALAPPDATA%\opencode-browser`
   - Linux/macOS: `~/.local/share/opencode-browser`
3. Проверьте: `opencode mcp list` — сервера быть не должно.

## Настройки, которые пригодятся

| Флаг | Зачем |
|---|---|
| `--headless` | без окна, только для парсинга |
| `--viewport-size 1280x720` | фиксированный размер окна |
| `--isolated` | не сохранять профиль после закрытия |
| `--ignore-https-errors` | игнорировать ошибки самоподписанных сертификатов |
| `--timeout-action 10000` | увеличить таймаут действий, мс |

Полный список: `npx -y @playwright/mcp@latest --help`.
