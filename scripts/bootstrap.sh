#!/usr/bin/env bash
# Настройка свежей Linux-машины одной командой.
#
#   bash scripts/bootstrap.sh
#   curl -fsSL https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.sh | bash
#
# Что делает: базовые пакеты -> nvm -> Node.js LTS + npm -> консольные утилиты -> настройка git.
#
# Переменные окружения:
#   SKIP_NODE=1    не устанавливать Node.js
#   SKIP_TOOLS=1   не устанавливать консольные утилиты
#   SKIP_GIT=1     не настраивать git
#
# Аргументы, переданные скрипту, уходят в setup-git.sh:
#   bash scripts/bootstrap.sh --name "Иван Иванов" --email "ivan@example.com"

set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts"

SKIP_NODE="${SKIP_NODE:-0}"
SKIP_TOOLS="${SKIP_TOOLS:-0}"
SKIP_GIT="${SKIP_GIT:-0}"

SELF="${BASH_SOURCE[0]:-}"
TMP_DIR=""
if [ -n "$SELF" ] && [ -f "$SELF" ]; then
  DIR="$(cd "$(dirname "$SELF")" && pwd)"
  LOCAL=1
else
  LOCAL=0
  TMP_DIR="$(mktemp -d)"
  trap 'rm -rf "$TMP_DIR"' EXIT
fi

step() { printf '\n===== %s =====\n' "$1"; }

script_path() {
  local name="$1"
  local path
  if [ "$LOCAL" = "1" ]; then
    path="$DIR/$name"
  else
    path="$TMP_DIR/$name"
    curl -fsSL "$REPO_RAW/$name" -o "$path"
  fi
  if [ ! -s "$path" ]; then
    echo "Ошибка: не удалось получить скрипт $name" >&2
    exit 1
  fi
  printf '%s\n' "$path"
}

if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi

# shellcheck disable=SC1091
. /etc/os-release 2>/dev/null || true
DISTRO="${ID:-} ${ID_LIKE:-}"

step "Дистрибутив"
echo "${PRETTY_NAME:-$(uname -s)} ($(uname -m))"

install_base() {
  case "$DISTRO" in
    *debian*|*ubuntu*)
      $SUDO apt-get update -y
      $SUDO apt-get install -y curl wget git unzip ca-certificates build-essential
      ;;
    *fedora*)
      $SUDO dnf install -y curl wget git unzip ca-certificates gcc gcc-c++ make
      ;;
    *arch*|*manjaro*)
      $SUDO pacman -Sy --noconfirm curl wget git unzip base-devel
      ;;
    *suse*)
      $SUDO zypper install -y curl wget git unzip ca-certificates gcc gcc-c++ make
      ;;
    *alpine*)
      $SUDO apk add curl wget git unzip ca-certificates build-base bash
      ;;
    *)
      echo "Дистрибутив не распознан. Установите вручную: curl, wget, git, unzip."
      return 0
      ;;
  esac
}

step "Базовые пакеты"
install_base

step "nvm"
bash "$(script_path install-nvm.sh)"

if [ "$SKIP_NODE" != "1" ]; then
  step "Node.js LTS + npm"
  bash "$(script_path update-node.sh)"
else
  echo "SKIP_NODE=1 — пропускаю Node.js"
fi

if [ "$SKIP_TOOLS" != "1" ]; then
  step "Консольные утилиты"
  bash "$(script_path install-cli-tools.sh)" || \
    echo "Утилиты установились не полностью — это не критично."
else
  echo "SKIP_TOOLS=1 — пропускаю утилиты"
fi

if [ "$SKIP_GIT" != "1" ]; then
  step "Настройка git"
  bash "$(script_path setup-git.sh)" "$@" || \
    echo "git настроен не полностью — запустите scripts/setup-git.sh позже."
else
  echo "SKIP_GIT=1 — пропускаю git"
fi

step "Готово"
echo "Откройте новый терминал и проверьте:"
echo "  node -v && npm -v && git --version"
echo
echo "OpenCode без установки:"
echo "  npx --yes @opencode/cli@latest"
echo
echo "Диагностика: bash scripts/check-env.sh"
