# Полезные консольные инструменты

Ставятся одной командой: [`scripts/install-cli-tools.sh`](../scripts/install-cli-tools.sh).

## Что и зачем

| Инструмент | Команда | Зачем |
|---|---|---|
| ripgrep | `rg` | быстрый поиск текста вместо `grep -r` |
| fd | `fd` | быстрый поиск файлов вместо `find` |
| bat | `bat` | `cat` с подсветкой синтаксиса |
| jq | `jq` | разбор JSON из API |
| tree | `tree` | структура папок |
| htop | `htop` | процессы, нагрузка, память |
| ncdu | `ncdu` | что занимает место на диске |
| tmux | `tmux` | несколько терминалов в одном окне |

## ripgrep

```bash
rg "def main"            # искать в текущей папке
rg -i "ошибка"           # без учёта регистра
rg -t py "import"        # только в .py
rg -l "TODO"             # только имена файлов
rg -n -C 2 "pattern"     # с номерами строк и контекстом
```

## fd

```bash
fd                     # все файлы рекурсивно
fd .py                 # все .py
fd -e json             # по расширению
fd -H config           # включая скрытые
fd -t d src            # только папки
fd -x rm {}            # выполнить команду для каждого файла
```

## bat

```bash
bat main.py
bat -p main.py         # без рамок и номеров строк
bat --diff файл        # подсветка изменений
```

## jq

```bash
curl -s https://api.github.com/repos/nodejs/node | jq '.stargazers_count'
jq '.users[] | .name' data.json
jq -r '.items[].id' data.json      # -r — без кавычек
jq 'keys' data.json
jq '.[] | select(.age > 18)' people.json
```

## tree

```bash
tree              # дерево текущей папки
tree -L 2         # только 2 уровня
tree -d           # только папки
tree -a           # включая скрытые
```

## htop

```bash
htop
```

`F6` — сортировка, `F9` — завершить процесс, `F10` — выход.

## ncdu

```bash
ncdu ~            # анализ домашней папки
ncdu /            # всей системы (может потребовать sudo)
```

Удаление прямо в интерфейсе: `d`. Выход: `q`.

## tmux

```bash
tmux                 # новая сессия
tmux ls              # список сессий
tmux attach -t 0     # вернуться в сессию
```

Внутри: `Ctrl+B`, затем `c` — новое окно, `n`/`p` — переключение, `%` — разделить вертикально, `"` — горизонтально, `d` — отсоединиться (сессия продолжит работать).

Полезно на удалённой машине: закрыли терминал — процесс жив.

## Алиасы

Добавить в `~/.bashrc`:

```bash
alias ll='ls -lah'
alias ..='cd ..'
alias ...='cd ../..'
alias gs='git status'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --all'
alias activate='source .venv/bin/activate'
alias py='python3'
```

Применить:

```bash
source ~/.bashrc
```

## bat и fd в Debian/Ubuntu

В репозиториях Ubuntu эти программы называются иначе: `batcat` и `fdfind`. Скрипт установки сам создаёт ссылки `bat` и `fd` в `~/.local/bin`. Вручную:

```bash
mkdir -p ~/.local/bin
ln -sf "$(command -v batcat)" ~/.local/bin/bat
ln -sf "$(command -v fdfind)" ~/.local/bin/fd
```
