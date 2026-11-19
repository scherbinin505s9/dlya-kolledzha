# для колледжа

Готовые команды для Linux: установка **nvm**, обновление **Node.js** и запуск **OpenCode через npx**.

Всё проверено на Ubuntu/Debian, Fedora, Arch, openSUSE и Alpine.
Актуально на ноябрь 2026: LTS-ветки Node.js — **26.x (Lithium)** и **24.x (Krypton)**.

## Содержание

1. [Проверка того, что уже установлено](#1-проверка-того-что-уже-установлено)
2. [Установка nvm](#2-установка-nvm)
3. [Обновление Node.js](#3-обновление-nodejs)
4. [Установка OpenCode через npx](#4-установка-opencode-через-npx)
5. [Если nvm не подходит: NodeSource и пакетные менеджеры](#5-если-nvm-не-подходит-nodesource-и-пакетные-менеджеры)
6. [Шпаргалка по командам](#6-шпаргалка-по-командам)
7. [Готовые скрипты](#7-готовые-скрипты)
8. [Проблемы и решения](#8-проблемы-и-решения)

---

## 1. Проверка того, что уже установлено

```bash
node -v          # версия Node.js
npm -v           # версия npm
which node       # откуда запускается node
cat /etc/os-release   # какой у вас дистрибутив Linux
```

Если `node -v` выдаёт что-то вроде `v18.x` — пришло время обновляться: Node.js 18 больше не поддерживается.

---

## 2. Установка nvm

**nvm** (Node Version Manager) — официальный способ держать несколько версий Node.js на одной машине и переключаться между ними.

### 2.1. Установка одной командой

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
```

Если `curl` не установлен:

```bash
sudo apt install -y curl      # Debian / Ubuntu
sudo dnf install -y curl      # Fedora
sudo pacman -S curl           # Arch
sudo zypper install curl      # openSUSE
sudo apk add curl             # Alpine
```

Альтернатива через `wget`:

```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
```

### 2.2. Подхватить nvm в текущем терминале

Установщик сам дописывает эти строки в `~/.bashrc` / `~/.zshrc`, но в **открытом** терминале нужно выполнить их вручную (или просто открыть новый терминал):

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"
```

### 2.3. Проверка

```bash
command -v nvm
nvm --version
```

Должно вывести `nvm` и номер версии. Команда `which nvm` **не работает** — nvm это функция оболочки, а не отдельный бинарник.

---

## 3. Обновление Node.js

### 3.1. Обновление до последней LTS (рекомендуется)

```bash
nvm install --lts
nvm alias default 'lts/*'
nvm use --lts
```

### 3.2. Перенос глобальных пакетов со старой версии

Чтобы не переустанавливать `npm i -g`-пакеты вручную:

```bash
nvm reinstall-packages-from=22.14.0   # подставьте свою старую версию (nvm ls)
```

Посмотреть, что установлено глобально на старой версии:

```bash
nvm use 22.14.0 && npm ls -g --depth=0
```

### 3.3. Обновление npm

```bash
npm install -g npm@latest
```

### 3.4. Другие варианты обновления

```bash
nvm install node              # последняя (не LTS) версия
nvm install 26                # конкретная мажорная версия
nvm install 24.22.3           # конкретная точная версия
nvm install --lts --reinstall-packages-from=node   # LTS + перенос пакетов
```

### 3.5. Удаление старых версий

```bash
nvm ls                 # что установлено
nvm uninstall 18       # удалить ненужную версию
nvm cache clear        # почистить кэш загрузок
```

### 3.6. Проверка результата

```bash
node -v
npm -v
nvm current
nvm ls
```

---

## 4. Установка OpenCode через npx

### 4.1. Запуск без установки (то, что просили)

```bash
npx @opencode/cli@latest
```

`npx` скачает актуальный пакет `@opencode/cli` во временный кэш и сразу запустит его.
Флаг `@latest` гарантирует свежую версию, а не старую из кэша.

С флагом `--yes`, чтобы npx не спрашивал подтверждение установки:

```bash
npx --yes @opencode/cli@latest
```

### 4.2. Постоянная установка (удобнее, если пользуетесь каждый день)

```bash
npm install -g @opencode/cli
opencode
```

Обновление глобально установленной версии:

```bash
npm update -g @opencode/cli
```

### 4.3. Альтернатива без Node.js вообще

```bash
curl -fsSL https://opencode.ai/v2/install | bash
```

### 4.4. Первый запуск

После старта в интерфейсе выполните:

```
/connect
```

и подключите провайдера модели (OpenCode Console, Anthropic, OpenAI и т.д.).

> **Важно:** старый пакет `opencode-ai` (команда `npx opencode-ai`) — это OpenCode V1.
> В V2 пакет называется `@opencode/cli`.

---

## 5. Если nvm не подходит: NodeSource и пакетные менеджеры

nvm — не единственный путь. Ниже — установка Node.js системно, через репозиторий дистрибутива.

### 5.1. Debian / Ubuntu (NodeSource)

```bash
# 1. Удалить старый Node.js из репозиториев Ubuntu
sudo apt-get purge -y nodejs npm
sudo apt-get autoremove -y

# 2. Подключить репозиторий NodeSource (замените 24 на 26 для текущей LTS)
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -

# 3. Установить
sudo apt-get install -y nodejs

# 4. Проверить
node -v
npm -v
```

### 5.2. Другие дистрибутивы

```bash
sudo dnf install -y nodejs npm                 # Fedora
sudo pacman -S nodejs npm                      # Arch
sudo zypper install nodejs22 npm               # openSUSE
sudo apk add nodejs npm                        # Alpine
```

### 5.3. Когда что выбирать

| Ситуация | Инструмент |
|---|---|
| Нужны разные версии Node.js для разных проектов | **nvm** |
| Один пользователь, учебные задачи | **nvm** |
| Сервер / Docker-образ | NodeSource или пакетный менеджер |
| Нет прав `sudo` | **nvm** (ставится в домашнюю папку) |

---

## 6. Шпаргалка по командам

### nvm

| Команда | Что делает |
|---|---|
| `nvm --version` | версия nvm |
| `nvm ls` | установленные версии |
| `nvm ls-remote` | все доступные версии |
| `nvm ls-remote --lts` | только LTS-версии |
| `nvm install --lts` | поставить последнюю LTS |
| `nvm install node` | поставить последнюю версию |
| `nvm use 24` | переключиться на версию 24 |
| `nvm alias default 'lts/*'` | LTS по умолчанию |
| `nvm current` | текущая активная версия |
| `nvm uninstall 18` | удалить версию |
| `nvm reinstall-packages-from=22` | перенести глобальные пакеты |
| `nvm cache clear` | очистить кэш |

### Node.js / npm

| Команда | Что делает |
|---|---|
| `node -v` | версия Node.js |
| `npm -v` | версия npm |
| `npm install -g npm@latest` | обновить npm |
| `npm ls -g --depth=0` | глобальные пакеты |
| `npm update -g @opencode/cli` | обновить OpenCode |

### OpenCode

| Команда | Что делает |
|---|---|
| `npx @opencode/cli@latest` | запуск без установки |
| `npm install -g @opencode/cli` | постоянная установка |
| `opencode` | запуск |
| `/connect` | подключить провайдера моделей |
| `curl -fsSL https://opencode.ai/v2/install \| bash` | установка без Node.js |

---

## 7. Готовые скрипты

В папке [`scripts/`](scripts) лежат те же команды в виде исполняемых файлов:

```bash
git clone <адрес-этого-репозитория>
cd dlya-kolledzha/scripts
chmod +x *.sh

./install-nvm.sh        # установить nvm
./update-node.sh        # обновить Node.js до LTS
./update-node.sh 26     # обновить до конкретной версии
./opencode-npx.sh       # запустить OpenCode через npx
./setup-all.sh          # всё сразу: nvm + Node.js LTS
./check-env.sh          # диагностика: что установлено и откуда
```

Скрипты можно запускать и без клонирования репозитория:

```bash
curl -fsSL https://raw.githubusercontent.com/<ваш-логин>/dlya-kolledzha/main/scripts/setup-all.sh | bash
```

---

## 8. Проблемы и решения

Подробный разбор — в [`docs/troubleshooting.md`](docs/troubleshooting.md).

Коротко:

| Проблема | Решение |
|---|---|
| `nvm: command not found` | открыть новый терминал или `source ~/.bashrc` |
| После `nvm use` версия не меняется | проверить `which node`, убрать системный Node из `PATH` |
| `nvm ls-remote` пустой | скачать `curl -fsSL https://nodejs.org/dist/index.json -o /dev/null` (нет доступа к nodejs.org) |
| OpenCode: `command not found` после npx | запускать `npx --yes @opencode/cli@latest` |
| `EACCES` при `npm i -g` | не использовать `sudo npm`; настраивать nvm или prefix |
| Windows | nvm из этого гайда — только Linux/macOS; на Windows нужен WSL |

---

## Лицензия

Материалы можно свободно использовать в учебных целях.
