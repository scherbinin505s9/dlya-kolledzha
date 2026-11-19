# Проблемы и решения

## nvm: command not found

**Причина:** nvm — это функция оболочки, она подгружается из `~/.nvm/nvm.sh` при старте терминала.

**Решение 1.** Открыть новый терминал.

**Решение 2.** Подгрузить вручную:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```

**Решение 3.** Проверить, что установщик дописал строки в конфиг оболочки:

```bash
tail -n 10 ~/.bashrc     # для bash
tail -n 10 ~/.zshrc      # для zsh
```

Если строк нет — добавить:

```bash
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> ~/.bashrc
source ~/.bashrc
```

---

## После `nvm use` версия Node.js не меняется

Проверить, откуда берётся `node`:

```bash
which node
type -a node
```

Если путь `/usr/bin/node` или `/usr/local/bin/node` — системный Node.js перекрывает nvm.

**Решение:** удалить системную установку, если она не нужна:

```bash
sudo apt-get purge -y nodejs npm     # Debian / Ubuntu
sudo dnf remove -y nodejs npm        # Fedora
```

Затем снова:

```bash
nvm use --lts
which node   # должно быть ~/.nvm/versions/node/v26.x.x/bin/node
```

Отдельный случай — **VS Code**: он запоминает `PATH` при запуске. После `nvm alias default` нужно полностью закрыть и открыть редактор.

---

## `nvm ls-remote` ничего не выводит или падает

nvm запрашивает список версий с `nodejs.org`.

```bash
# проверить доступ
curl -I https://nodejs.org/dist/index.json
```

**Если ошибка 403 / таймаут:** сеть блокирует запросы. Варианты:

```bash
# 1. указать зеркало
export NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node
nvm ls-remote --lts

# 2. проверить прокси
echo $http_proxy $https_proxy
```

---

## Установка nvm падает с ошибкой про `git`

Старый установщик использовал `git clone`. Обновите команду до актуальной (v0.41.0):

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
```

---

## `npm install -g` падает с `EACCES: permission denied`

**Не используйте `sudo npm install -g`** — это ломает права на файлы и кэш.

Правильные варианты:

**Вариант 1 (рекомендуется).** Работать через nvm — там глобальные пакеты ставятся в домашнюю папку:

```bash
nvm install --lts
npm install -g @opencode/cli
```

**Вариант 2.** Сменить папку глобальных пакетов:

```bash
mkdir -p ~/.npm-global
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## OpenCode: `command not found` или `npx` ругается

Запуск без установки:

```bash
npx --yes @opencode/cli@latest
```

Если npx не находит пакет:

```bash
npm config get registry          # должен быть https://registry.npmjs.org/
npm cache clean --force
```

Постоянная установка:

```bash
npm install -g @opencode/cli
hash -r          # сбросить кэш путей оболочки
opencode
```

Проверить, что бинарник на месте:

```bash
npm ls -g --depth=0 | grep opencode
which opencode
```

---

## OpenCode запускается, но не подключается провайдер моделей

Внутри интерфейса:

```
/connect
```

и выбрать провайдера. Для OpenCode Console / Anthropic / OpenAI потребуется вход или API-ключ.

Проверить конфигурацию:

```
opencode service status
```

Логи:

```bash
cat ~/.local/share/opencode/log/opencode.log | tail -n 100
```

---

## Node.js установлен, но `npm` показывает другую версию

`npm` идёт в комплекте с версией Node.js. Если версии расходятся:

```bash
which npm
npm -v
node -v
```

Скорее всего в `PATH` остался старый npm из `/usr/bin`. Убирается удалением системного пакета или правкой `PATH`.

Обновить npm до последней версии:

```bash
npm install -g npm@latest
```

---

## Windows

nvm из этого руководства (`nvm-sh`) работает **только на Linux и macOS**.

На Windows есть три пути:

1. **WSL** (рекомендуется):

```powershell
wsl --install -d Ubuntu
```

Далее внутри Ubuntu выполнять все команды из этого репозитория.

2. **nvm-windows** — другой проект, другой набор команд:

```powershell
winget install CoreyButler.NVMforWindows
```

3. **Git Bash** — работает частично, установщик nvm может не найти `~/.bashrc`.

---

## Как полностью удалить nvm и начать заново

```bash
# удалить папку nvm
rm -rf "$NVM_DIR"

# убрать строки nvm из конфига оболочки
sed -i '/NVM_DIR/d' ~/.bashrc
sed -i '/nvm.sh/d' ~/.bashrc
sed -i '/bash_completion/d' ~/.bashrc

# открыть новый терминал
```
