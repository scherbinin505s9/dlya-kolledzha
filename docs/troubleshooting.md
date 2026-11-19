# Частые ошибки

По темам: [Linux](#linux), [Git](#git), [Python](#python), [Docker](#docker), [Node.js](#nodejs), [VS Code](#vs-code).

## Linux

### `Permission denied`

```bash
ls -l файл          # посмотреть права
chmod +x файл       # если это скрипт
sudo команда        # если действие требует администратора
```

Если файл принадлежит другому пользователю:

```bash
sudo chown -R "$USER":"$USER" папка
```

### `Could not get lock /var/lib/dpkg/lock-frontend`

Другой процесс уже работает с `apt`:

```bash
sudo killall apt apt-get
sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock*
sudo dpkg --configure -a
sudo apt update
```

### `No space left on device`

```bash
df -h               # где закончилось место
ncdu ~              # что занимает
sudo apt autoremove -y
sudo apt clean
```

### `command not found`, хотя пакет установлен

```bash
which команда
echo $PATH
hash -r             # сбросить кэш путей
```

Часто помогает открыть новый терминал.

### `bash: ./script.sh: /bin/bash^M: bad interpreter`

Скрипт сохранён с виндовыми переводами строк:

```bash
sed -i 's/\r$//' script.sh
# или
sudo apt install -y dos2unix && dos2unix script.sh
```

## Git

### `rejected ... non-fast-forward`

```bash
git pull --rebase
git push
```

### `Please tell me who you are`

```bash
git config --global user.name "Имя Фамилия"
git config --global user.email "почта@example.com"
```

### `Permission denied (publickey)`

```bash
ssh -T git@github.com
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub      # ключ должен быть добавлен на GitHub
```

### `fatal: not a git repository`

```bash
cd папка-проекта
git init
```

### Случайно закоммитил пароль или `.env`

```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "убрать .env из репозитория"
```

Пароль всё равно остался в истории — сменить его. Для новых проектов сразу создавать `.gitignore`.

## Python

### `externally-managed-environment`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install пакет
```

### `ModuleNotFoundError`, хотя пакет установлен

Пакет стоит в другом окружении:

```bash
which python3
pip -V
```

Оба пути должны указывать внутрь `.venv`.

### `No module named venv`

```bash
sudo apt install -y python3-venv
```

### `IndentationError`

Смешаны табы и пробелы. В VS Code: `Ctrl+Shift+P` → **Convert Indentation to Spaces**, размер 4.

## Docker

### `permission denied ... /var/run/docker.sock`

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### `port is already allocated`

```bash
ss -tulpn | grep 8080
docker run -p 8081:80 ...
```

### `Cannot connect to the Docker daemon`

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Node.js

### `nvm: command not found`

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```

Подробно — [node-nvm-opencode.md](node-nvm-opencode.md#проблемы).

### `EACCES` при `npm install -g`

Не использовать `sudo npm`. Настроить nvm или свой prefix:

```bash
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### `npm ERR! code EJSONPARSE`

Сломан `package.json` (лишняя запятая, комментарий). Проверить:

```bash
node -e "JSON.parse(require('fs').readFileSync('package.json'))"
```

### Забыл `npm install` после `git clone`

```bash
npm install
```

## VS Code

### `code: command not found`

`Ctrl+Shift+P` → **Shell Command: Install 'code' command in PATH**.

### Терминал VS Code не видит Node из nvm

Полностью закрыть и открыть VS Code — он запоминает `PATH` при старте.

### Расширение Python не видит `.venv`

`Ctrl+Shift+P` → **Python: Select Interpreter** → выбрать путь `.venv/bin/python`.
Проверить, что окружение создано **внутри** папки проекта.

### Файлы в Git изменились сами (CRLF → LF)

```bash
git config --global core.autocrlf input   # Linux
git config --global core.autocrlf true    # Windows
```

## Универсальное

Не понимаю, что не так — начните с диагностики:

```bash
bash scripts/check-env.sh
```

Она покажет ОС, версии node/npm/nvm, `PATH`, registry и глобальные пакеты.
