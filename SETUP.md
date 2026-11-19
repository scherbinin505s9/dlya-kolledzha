# Установка и настройка

Что делает `bootstrap`, как пропустить лишнее и что проверить после установки.

## Linux: одна команда

```bash
curl -fsSL https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.sh | bash
```

Или из клонированного репозитория:

```bash
bash scripts/bootstrap.sh
```

### Порядок действий

| Шаг | Что происходит |
|---|---|
| 1 | Определяется дистрибутив по `/etc/os-release` |
| 2 | Ставятся базовые пакеты: `curl`, `wget`, `git`, `unzip`, компиляторы |
| 3 | Ставится nvm в `~/.nvm` |
| 4 | Ставится последняя LTS Node.js, обновляется npm, LTS становится версией по умолчанию |
| 5 | Ставятся `rg`, `fd`, `bat`, `jq`, `tree`, `htop`, `ncdu`, `tmux` |
| 6 | Настраивается git: имя, почта, ветка `main`, алиасы |

`sudo` попросит пароль только на шагах 2 и 5. nvm и Node.js ставятся в домашнюю папку пользователя.

### Пропустить ненужное

```bash
SKIP_NODE=1  bash scripts/bootstrap.sh    # без Node.js
SKIP_TOOLS=1 bash scripts/bootstrap.sh    # без консольных утилит
SKIP_GIT=1   bash scripts/bootstrap.sh    # без настройки git
```

### Сразу указать данные для git

```bash
bash scripts/bootstrap.sh --name "Иван Иванов" --email "ivan@example.com"
```

Если запускать через `curl | bash` и не передать имя с почтой, шаг с git будет пропущен (терминал неинтерактивный).
Позже это делается командой:

```bash
scripts/setup-git.sh --name "Иван Иванов" --email "ivan@example.com" --ssh
```

### Без интернета

Скрипт скачивает nvm и пакеты из сети. Если на лабораторной машине интернета нет, установка не пройдёт —
используйте раздел [windows-wsl.md](docs/windows-wsl.md) для домашней машины или заранее скачанные пакеты.

## Windows: одна команда

```powershell
irm https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.ps1 | iex
```

Из клонированного репозитория:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

| Параметр | Что делает |
|---|---|
| `-SkipPython` | не ставить Python |
| `-SkipVSCode` | не ставить VS Code |
| `-DryRun` | показать список пакетов без установки |

Ставит: Git, Node.js LTS, Windows Terminal, 7-Zip, VS Code, Python 3.14.
Пакеты ставятся через `winget`, права администратора обычно не нужны.

Если нужен полноценный Linux — установите WSL:

```powershell
wsl --install -d Ubuntu
```

Подробнее: [windows-wsl.md](docs/windows-wsl.md).

## Проверка после установки

Откройте **новый** терминал (старый не увидит изменения `PATH`):

```bash
node -v
npm -v
git --version
rg --version
nvm --version
```

Ожидается: Node.js 26.x (LTS), npm 11.x, git 2.x.

Полная диагностика:

```bash
bash scripts/check-env.sh
```

Она печатает дистрибутив, версии, откуда запускается `node`, `PATH`, registry npm и глобальные пакеты.

## Ручная установка по шагам

Если не хочется запускать `bootstrap` целиком:

```bash
bash scripts/install-nvm.sh          # 1. nvm
bash scripts/update-node.sh          # 2. Node.js LTS
bash scripts/install-cli-tools.sh    # 3. утилиты
bash scripts/setup-git.sh --ssh      # 4. git
bash scripts/install-dotnet.sh 8.0   # 5. .NET SDK для C# (необязательно)
```

.NET ставится без root в `~/.dotnet`. Версию берите ту, что требует преподаватель:
`10.0` — текущий LTS, `8.0` — если в колледже старые методички.

OpenCode ставится одной командой:

```bash
npm install -g @opencode/cli
```

Запуск из папки репозитория:

```bash
cd dlya-kolledzha
opencode
```

Если Node.js ещё нет, сначала запустите `bootstrap` или скачайте LTS с
[nodejs.org](https://nodejs.org/).

## Удаление

Полностью убрать nvm и Node.js:

```bash
rm -rf "$HOME/.nvm"
sed -i '/NVM_DIR/d; /nvm.sh/d; /bash_completion/d' ~/.bashrc
```

Утилиты удаляются пакетным менеджером:

```bash
sudo apt remove -y ripgrep fd-find bat jq tree htop ncdu tmux
```
