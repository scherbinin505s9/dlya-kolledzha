#!/usr/bin/env bash
# Настройка git: имя, почта, ветка по умолчанию, алиасы, SSH-ключ.
#
#   ./setup-git.sh
#   ./setup-git.sh --name "Иван Иванов" --email "ivan@example.com"
#   ./setup-git.sh --ssh          # дополнительно создать SSH-ключ
#
# Без аргументов спрашивает имя и почту (если запущено в интерактивном терминале).

set -euo pipefail

NAME=""
EMAIL=""
MAKE_SSH=0

usage() {
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case "$1" in
    --name)  NAME="${2:-}"; shift 2 ;;
    --email) EMAIL="${2:-}"; shift 2 ;;
    --ssh)   MAKE_SSH=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Неизвестный аргумент: $1" >&2; exit 1 ;;
  esac
done

if ! command -v git >/dev/null 2>&1; then
  echo "Ошибка: git не установлен." >&2
  echo "  Debian/Ubuntu: sudo apt install -y git" >&2
  exit 1
fi

[ -z "$NAME" ]  && NAME="$(git config --global user.name 2>/dev/null || true)"
[ -z "$EMAIL" ] && EMAIL="$(git config --global user.email 2>/dev/null || true)"

if [ -z "$NAME" ] || [ -z "$EMAIL" ]; then
  if [ -t 0 ]; then
    [ -z "$NAME" ]  && read -r -p "Имя для git (как на GitHub): " NAME
    [ -z "$EMAIL" ] && read -r -p "Почта для git: " EMAIL
  else
    echo "git: имя и почта не заданы, а терминал неинтерактивный."
    echo "Позже выполните: ./setup-git.sh --name \"Имя\" --email \"почта\""
  fi
fi

if [ -n "$NAME" ] && [ -n "$EMAIL" ]; then
  git config --global user.name "$NAME"
  git config --global user.email "$EMAIL"
  echo "git: $NAME <$EMAIL>"
fi

git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input
git config --global core.editor "nano"

git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD --stat"

echo "Алиасы: git st, git co, git br, git lg, git last"

if [ "$MAKE_SSH" = "1" ]; then
  KEY="$HOME/.ssh/id_ed25519"
  if [ -f "$KEY" ]; then
    echo "SSH-ключ уже существует: $KEY"
  else
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    ssh-keygen -t ed25519 -N "" -C "${EMAIL:-$USER@$(hostname)}" -f "$KEY"
  fi
  echo
  echo "Публичный ключ (добавьте на GitHub → Settings → SSH and GPG keys):"
  echo "----------------------------------------------------------------"
  cat "$KEY.pub"
  echo "----------------------------------------------------------------"
  echo "Проверка: ssh -T git@github.com"
fi

echo
echo "Готово. Проверить: git config --list --show-origin"
