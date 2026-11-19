# для колледжа

Личная база для учёбы: настройка свежего компьютера одной командой, шпаргалки по темам и готовые скрипты.
Чтобы не повторять одно и то же на каждой лабораторной машине.

## Быстрый старт

**Linux** (Ubuntu, Debian, Fedora, Arch, openSUSE, Alpine):

```bash
curl -fsSL https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.sh | bash
```

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.ps1 | iex
```

После установки откройте **новый** терминал и проверьте:

```bash
node -v && npm -v && git --version
```

OpenCode запускается сразу, без установки:

```bash
npx --yes @opencode/cli@latest
```

Что именно ставится и как пропустить лишнее — в [SETUP.md](SETUP.md).

---

## Разделы

| # | Тема | О чём |
|---|---|---|
| 01 | [Linux: база](docs/linux-basics.md) | файлы, права, пакеты, процессы, порты, сеть, архивы |
| 02 | [Node.js: nvm, обновление, OpenCode](docs/node-nvm-opencode.md) | установка nvm, LTS, перенос пакетов, `npx @opencode/cli` |
| 03 | [Git и GitHub](docs/git-github.md) | настройка, SSH-ключ, ветки, откат, типичные ошибки |
| 04 | [Python](docs/python.md) | venv, pip, Jupyter, PEP 668, структура проекта |
| 05 | [Docker](docs/docker.md) | установка без sudo, контейнеры, compose, сборка образов |
| 06 | [VS Code](docs/vscode.md) | установка, расширения, настройки, Remote-SSH |
| 07 | [Консольные утилиты](docs/cli-tools.md) | rg, fd, bat, jq, tree, htop, ncdu, tmux, алиасы |
| 08 | [Windows и WSL](docs/windows-wsl.md) | winget, WSL, файлы, VS Code + WSL |
| 09 | [Частые ошибки](docs/troubleshooting.md) | сводка по всем темам: что писать, когда всё сломалось |

## Скрипты

```bash
git clone https://github.com/scherbinin505s9/dlya-kolledzha.git
cd dlya-kolledzha/scripts
chmod +x *.sh
```

| Скрипт | Что делает |
|---|---|
| `bootstrap.sh` | всё сразу на Linux: пакеты → nvm → Node LTS → утилиты → git |
| `bootstrap.ps1` | всё сразу на Windows через winget |
| `install-nvm.sh` | ставит nvm v0.41.0 |
| `update-node.sh` | Node.js до LTS (или указанной версии) + перенос глобальных пакетов |
| `opencode-npx.sh` | запуск `npx @opencode/cli@latest` |
| `install-cli-tools.sh` | rg, fd, bat, jq, tree, htop, ncdu, tmux |
| `setup-git.sh` | имя, почта, ветка `main`, алиасы, SSH-ключ (`--ssh`) |
| `check-env.sh` | диагностика: ОС, node, npm, nvm, PATH, registry |

Примеры:

```bash
./bootstrap.sh                                  # всё
SKIP_TOOLS=1 ./bootstrap.sh                     # без консольных утилит
./bootstrap.sh --name "Иван Иванов" --email "ivan@example.com"
./update-node.sh 24                             # конкретная версия
./setup-git.sh --ssh                            # настройка git + ключ
```

## Структура

```
dlya-kolledzha/
├── README.md                  # эта страница
├── SETUP.md                   # что делает bootstrap и как его настроить
├── docs/                      # шпаргалки по темам
│   ├── linux-basics.md
│   ├── node-nvm-opencode.md
│   ├── git-github.md
│   ├── python.md
│   ├── docker.md
│   ├── vscode.md
│   ├── cli-tools.md
│   ├── windows-wsl.md
│   └── troubleshooting.md
└── scripts/                   # готовые команды
    ├── bootstrap.sh
    ├── bootstrap.ps1
    ├── install-nvm.sh
    ├── update-node.sh
    ├── opencode-npx.sh
    ├── install-cli-tools.sh
    ├── setup-git.sh
    └── check-env.sh
```

## Как добавить свой раздел

1. Создать `docs/название.md` — коротко, командами, без воды.
2. Добавить строку в таблицу «Разделы» выше.
3. Закоммитить:

```bash
git add docs/название.md README.md
git commit -m "добавить раздел про ..."
git push
```

Правила, чтобы репозиторий оставался полезным:

- команда должна быть готова к копированию, без «подставьте своё» там, где можно обойтись без этого;
- в каждом разделе — блок «Частые ошибки»;
- никаких паролей, токенов и личных данных в файлах.

## Идеи для будущих разделов

- [ ] C/C++: gcc, g++, make, отладка в VS Code
- [ ] Java: JDK, Maven, запуск лабораторных
- [ ] SQL: PostgreSQL и MySQL в Docker, шпаргалка по запросам
- [ ] Сети: `ip`, `ss`, `tcpdump`, Wireshark
- [ ] Алгоритмы и структуры данных: шаблоны на Python/C++
- [ ] LaTeX и оформление отчётов
- [ ] Bash-скрипты: циклы, условия, аргументы

## Лицензия

Материалы можно свободно использовать в учебных целях.
