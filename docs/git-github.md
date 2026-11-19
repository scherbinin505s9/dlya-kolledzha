# Git и GitHub

## Установка

```bash
sudo apt install -y git     # Debian / Ubuntu
sudo dnf install -y git     # Fedora
sudo pacman -S git          # Arch
```

Проверка:

```bash
git --version
```

## Первичная настройка (один раз на компьютере)

```bash
git config --global user.name "Имя Фамилия"
git config --global user.email "почта@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input   # Linux/macOS
```

На Windows правильнее `core.autocrlf true` — иначе файлы будут с CRLF и bash-скрипты сломаются.

Проверить, что записалось:

```bash
git config --list --show-origin
```

Готовый скрипт: [`scripts/setup-git.sh`](../scripts/setup-git.sh).

## Ключ SSH к GitHub

Без него каждый `push` будет просить пароль.

```bash
ssh-keygen -t ed25519 -C "почта@example.com"   # Enter Enter Enter
cat ~/.ssh/id_ed25519.pub
```

Скопированный ключ вставить на GitHub: **Settings → SSH and GPG keys → New SSH key**.

Проверка:

```bash
ssh -T git@github.com
# Hi <логин>! You've successfully authenticated...
```

Через HTTPS проще, если установлен GitHub CLI:

```bash
gh auth login
```

## Ежедневный цикл

```bash
git status                 # что изменилось
git add файл               # подготовить файл
git add .                  # подготовить всё
git commit -m "сообщение"  # зафиксировать
git push                   # отправить на GitHub
git pull                   # забрать чужие изменения
```

## Ветки

```bash
git branch                 # локальные ветки
git branch feature         # создать
git switch feature         # переключиться (или git checkout)
git switch -c feature      # создать и сразу переключиться
git merge feature          # влить в текущую ветку
git branch -d feature      # удалить после слияния
```

## Первый репозиторий

```bash
mkdir проект && cd проект
git init
git add .
git commit -m "первый коммит"
gh repo create проект --public --source . --push   # через GitHub CLI
```

Без `gh`:

```bash
git remote add origin git@github.com:логин/проект.git
git branch -M main
git push -u origin main
```

## Откат изменений

```bash
git restore файл                 # вернуть файл из последнего коммита
git restore --staged файл        # убрать из подготовленных
git reset --hard HEAD            # выбросить ВСЕ незакоммиченные изменения
git revert <hash>                # отменить коммит новым коммитом (безопасно)
git log --oneline --graph --all  # история
```

`git reset --hard` необратим для незакоммиченных файлов. Перед ним: `git stash`.

```bash
git stash        # спрятать изменения
git stash pop    # вернуть
```

## .gitignore

```
node_modules/
.venv/
__pycache__/
*.log
.env
.vscode/
```

Проверить, что файл не попал в репозиторий:

```bash
git ls-files | grep .env
```

Если попал — удалить из индекса, оставив на диске:

```bash
git rm --cached .env
```

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `rejected ... non-fast-forward` | на GitHub есть коммиты, которых нет локально | `git pull --rebase`, затем `git push` |
| `fatal: not a git repository` | команда не в папке проекта | `cd` в проект или `git init` |
| `Please tell me who you are` | не заданы `user.name` / `user.email` | выполнить настройку выше |
| `Permission denied (publickey)` | не добавлен SSH-ключ | `ssh-add ~/.ssh/id_ed25519`, проверить ключ на GitHub |
| `HEAD detached` | переключились на коммит, а не на ветку | `git switch main` |
| `LF will be replaced by CRLF` | настройка переводов строк | на Linux `core.autocrlf input` |
| `failed to push some refs` | нет прав на чужой репозиторий | сделать fork и пушить в свой |
