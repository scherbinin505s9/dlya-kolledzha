# Node.js: nvm, обновление, OpenCode через npx

Актуально на ноябрь 2026: LTS-ветки Node.js — **26.x (Lithium)** и **24.x (Krypton)**.

## Проверить, что уже стоит

```bash
node -v
npm -v
which node
```

Если `node -v` выдаёт `v18.x` или ниже — пора обновляться: Node.js 18 больше не поддерживается.

## Установка nvm

**nvm** — официальный способ держать несколько версий Node.js и переключаться между ними. Ставится в домашнюю папку, `sudo` не нужен.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
```

Без `curl`:

```bash
sudo apt install -y curl      # Debian / Ubuntu
sudo dnf install -y curl      # Fedora
sudo pacman -S curl           # Arch
sudo zypper install curl      # openSUSE
sudo apk add curl             # Alpine
```

Или через `wget`:

```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
```

Подхватить в **текущем** терминале (установщик дописывает это в `~/.bashrc` / `~/.zshrc`):

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"
```

Проверка:

```bash
command -v nvm     # выведет: nvm
nvm --version
```

`which nvm` не работает — nvm это функция оболочки, а не бинарник.

## Обновление Node.js

### До последней LTS (обычный случай)

```bash
nvm install --lts
nvm alias default 'lts/*'
nvm use --lts
```

### Перенос глобальных пакетов

```bash
nvm reinstall-packages-from=22.14.0   # свою старую версию смотрите в nvm ls
```

Посмотреть, что стоит глобально:

```bash
nvm use 22.14.0 && npm ls -g --depth=0
```

### Обновить npm

```bash
npm install -g npm@latest
```

### Другие варианты

```bash
nvm install node              # последняя версия, не LTS
nvm install 26                # конкретная мажорная
nvm install 24.22.3           # конкретная точная
nvm install --lts --reinstall-packages-from=node
```

### Удалить старое

```bash
nvm ls
nvm uninstall 18
nvm cache clear
```

### Проверка

```bash
node -v
npm -v
nvm current
```

## OpenCode через npx

### Запуск без установки

```bash
npx @opencode/cli@latest
```

`npx` скачает актуальный пакет во временный кэш и сразу запустит. `@latest` гарантирует свежую версию.

Без вопроса о подтверждении установки:

```bash
npx --yes @opencode/cli@latest
```

### Постоянная установка

```bash
npm install -g @opencode/cli
opencode
```

Обновление:

```bash
npm update -g @opencode/cli
```

### Без Node.js вообще

```bash
curl -fsSL https://opencode.ai/v2/install | bash
```

### Первый запуск

В интерфейсе выполнить `/connect` и подключить провайдера моделей.

> Старый пакет `opencode-ai` (команда `npx opencode-ai`) — это OpenCode V1.
> В V2 пакет называется **`@opencode/cli`**.

## Если nvm не подходит

### Debian / Ubuntu (NodeSource)

```bash
sudo apt-get purge -y nodejs npm
sudo apt-get autoremove -y
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -   # 24 → 26 для текущей LTS
sudo apt-get install -y nodejs
node -v
```

### Другие дистрибутивы

```bash
sudo dnf install -y nodejs npm      # Fedora
sudo pacman -S nodejs npm           # Arch
sudo zypper install nodejs22 npm    # openSUSE
sudo apk add nodejs npm             # Alpine
```

### Когда что выбирать

| Ситуация | Инструмент |
|---|---|
| Разные версии Node.js для разных проектов | **nvm** |
| Учебные задачи, один пользователь | **nvm** |
| Сервер / Docker-образ | NodeSource или пакетный менеджер |
| Нет прав `sudo` | **nvm** |

## Шпаргалка

### nvm

| Команда | Что делает |
|---|---|
| `nvm ls` | установленные версии |
| `nvm ls-remote --lts` | доступные LTS-версии |
| `nvm install --lts` | поставить последнюю LTS |
| `nvm use 24` | переключиться на 24 |
| `nvm alias default 'lts/*'` | LTS по умолчанию |
| `nvm current` | текущая версия |
| `nvm uninstall 18` | удалить версию |
| `nvm reinstall-packages-from=22` | перенести глобальные пакеты |
| `nvm cache clear` | очистить кэш |

### OpenCode

| Команда | Что делает |
|---|---|
| `npx @opencode/cli@latest` | запуск без установки |
| `npm install -g @opencode/cli` | постоянная установка |
| `opencode` | запуск |
| `/connect` | подключить провайдера моделей |

## Проблемы

### `nvm: command not found`

```bash
source ~/.bashrc          # или открыть новый терминал
tail -n 10 ~/.bashrc      # проверить, что установщик дописал строки
```

### После `nvm use` версия не меняется

```bash
which node      # если /usr/bin/node — системный Node перекрывает nvm
sudo apt-get purge -y nodejs npm
```

VS Code запоминает `PATH` при запуске — после смены версии его надо полностью перезапустить.

### `EACCES` при `npm install -g`

Не использовать `sudo npm`. Правильно — работать через nvm (пакеты ставятся в домашнюю папку) или задать свой prefix:

```bash
mkdir -p ~/.npm-global
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### `nvm ls-remote` пустой

```bash
curl -I https://nodejs.org/dist/index.json     # проверить доступ
export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node
```

### OpenCode не находится после npx

```bash
npm config get registry     # должно быть https://registry.npmjs.org/
npm cache clean --force
npx --yes @opencode/cli@latest
```

### Windows

nvm из этого гайда работает только на Linux/macOS. На Windows нужен WSL — см. [windows-wsl.md](windows-wsl.md).
