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

Карта «предмет → раздел» под специальность **09.02.07 Информационные системы
и программирование** (колледж АлтГУ): [docs/asu-isp.md](docs/asu-isp.md).

### Настройка и инструменты

| # | Тема | О чём |
|---|---|---|
| 01 | [Linux: база](docs/linux-basics.md) | файлы, права, пакеты, процессы, порты, сеть, архивы |
| 02 | [Node.js: nvm, обновление, OpenCode](docs/node-nvm-opencode.md) | установка nvm, LTS, перенос пакетов, `npx @opencode/cli` |
| 03 | [Git и GitHub](docs/git-github.md) | настройка, SSH-ключ, ветки, откат, типичные ошибки |
| 04 | [Python](docs/python.md) | venv, pip, Jupyter, Tkinter/PyQt, PEP 668, структура проекта |
| 05 | [Docker](docs/docker.md) | установка без sudo, контейнеры, compose, сборка образов |
| 06 | [VS Code](docs/vscode.md) | установка, расширения, настройки, Remote-SSH |
| 07 | [Консольные утилиты](docs/cli-tools.md) | rg, fd, bat, jq, tree, htop, ncdu, tmux, алиасы |
| 08 | [Windows и WSL](docs/windows-wsl.md) | winget, WSL, файлы, VS Code + WSL |
| 09 | [Частые ошибки](docs/troubleshooting.md) | сводка по всем темам: что писать, когда всё сломалось |

### Предметы 09.02.07

| # | Тема | Предмет |
|---|---|---|
| 10 | [Карта специальности](docs/asu-isp.md) | текущие курсы с портала → разделы |
| 11 | [Алгоритмы и Python](docs/algorithms.md) | Основы алгоритмизации и программирования |
| 12 | [Базы данных и SQL](docs/databases-sql.md) | Основы проектирования баз данных |
| 13 | [Веб и интерфейсы](docs/web-basics.md) | Основы веб-технологий, ПиРИП |
| 14 | [Linux, Windows, PowerShell](docs/windows-wsl.md) | Операционные системы и среды |
| 15 | [Отчёты и документация](docs/reports-gost.md) | все предметы |
| 16 | [C# и .NET](docs/csharp-dotnet.md) | на будущее / демоэкзамен |
| 17 | [Компьютерные сети](docs/networks.md) | на будущее |
| 18 | [Тестирование и QA](docs/testing-qa.md) | на будущее / демоэкзамен |
| 19 | [Архитектура и информатика](docs/hardware.md) | Информатика |

## Отправленные задания

Выполненные и сданные работы — в папке
[«Отправленные задания»](Отправленные%20задания/README.md). У каждой работы свой
`README.md`: что требовалось, что сделано, дата сдачи и статус в Moodle.

| Предмет | Работа | Дата | Статус |
|---|---|---|---|
| ПиРИП | [Создание формы на html-странице](Отправленные%20задания/ПиРИП/Создание%20формы%20на%20html-странице/README.md) | 19.11.2026 | Отправлено для оценивания |

## Скилл для агента: браузер

В [.opencode/skills/browser-control/](.opencode/skills/browser-control/SKILL.md) лежит готовый скилл:
агент учится открывать сайты, читать страницы, кликать, заполнять формы
и снимать скриншоты через Playwright MCP.

- [SKILL.md](.opencode/skills/browser-control/SKILL.md) — правила работы;
- [references/setup.md](.opencode/skills/browser-control/references/setup.md) — как подключить MCP;
- [references/tools.md](.opencode/skills/browser-control/references/tools.md) — все инструменты.

Проверка подключения:

```bash
opencode mcp list
```

Ожидается `✓ playwright connected`. Скилл подхватывается автоматически, когда
OpenCode открыт в папке этого репозитория.

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
| `install-dotnet.sh` | .NET SDK без root (по умолчанию 10.0, можно `8.0`) |
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
├── AGENTS.md                  # правила для агента: как делать учебные работы
├── SETUP.md                   # что делает bootstrap и как его настроить
├── .opencode/
│   └── skills/
│       └── browser-control/   # скилл: управление браузером
│           ├── SKILL.md
│           └── references/
├── Отправленные задания/      # сданные лабораторные
│   ├── README.md              # список работ и правила
│   └── ПиРИП/
│       └── Создание формы на html-странице/
│           ├── README.md
│           ├── form.html
│           ├── образец.png
│           └── результат.png
├── docs/                      # шпаргалки по темам
│   ├── asu-isp.md             # карта специальности 09.02.07
│   ├── linux-basics.md
│   ├── node-nvm-opencode.md
│   ├── git-github.md
│   ├── python.md
│   ├── docker.md
│   ├── vscode.md
│   ├── cli-tools.md
│   ├── windows-wsl.md
│   ├── algorithms.md
│   ├── csharp-dotnet.md
│   ├── databases-sql.md
│   ├── networks.md
│   ├── testing-qa.md
│   ├── web-basics.md
│   ├── hardware.md
│   ├── reports-gost.md
│   └── troubleshooting.md
└── scripts/                   # готовые команды
    ├── bootstrap.sh
    ├── bootstrap.ps1
    ├── install-nvm.sh
    ├── update-node.sh
    ├── opencode-npx.sh
    ├── install-cli-tools.sh
    ├── install-dotnet.sh
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
- [ ] Мобильная разработка (МДК.01.03): Kotlin + Android Studio или Flutter
- [ ] Численные методы (ОП.10): реализация на Python
- [ ] ИИ и большие данные (ОП.13): pandas, основы моделей
- [ ] Управление IT-проектами (ОП.15): Scrum, Kanban, Trello
- [ ] Bash-скрипты: циклы, условия, аргументы

## Лицензия

Материалы можно свободно использовать в учебных целях.
