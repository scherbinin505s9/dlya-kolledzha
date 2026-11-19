#!/usr/bin/env bash
# Установка полезных консольных утилит.
#
#   ./install-cli-tools.sh
#
# Ставит: ripgrep (rg), fd, bat, jq, tree, htop, ncdu, tmux.
# В Debian/Ubuntu bat называется batcat, fd — fdfind; скрипт создаёт
# привычные ссылки bat и fd в ~/.local/bin.

set -euo pipefail

if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi

# shellcheck disable=SC1091
. /etc/os-release 2>/dev/null || true
DISTRO="${ID:-} ${ID_LIKE:-}"

echo "Дистрибутив: ${PRETTY_NAME:-$(uname -s)}"

install_tools() {
  case "$DISTRO" in
    *debian*|*ubuntu*)
      $SUDO apt-get update -y
      $SUDO apt-get install -y ripgrep fd-find bat jq tree htop ncdu tmux
      ;;
    *fedora*)
      $SUDO dnf install -y ripgrep fd-find bat jq tree htop ncdu tmux
      ;;
    *arch*|*manjaro*)
      $SUDO pacman -Sy --noconfirm ripgrep fd bat jq tree htop ncdu tmux
      ;;
    *suse*)
      $SUDO zypper install -y ripgrep fd bat jq tree htop ncdu tmux
      ;;
    *alpine*)
      $SUDO apk add ripgrep fd bat jq tree htop ncdu tmux
      ;;
    *)
      echo "Дистрибутив не распознан. Установите вручную: ripgrep fd bat jq tree htop ncdu tmux"
      return 1
      ;;
  esac
}

install_tools || exit 1

# Debian/Ubuntu: привычные имена вместо batcat / fdfind
mkdir -p "$HOME/.local/bin"
if command -v batcat >/dev/null 2>&1 && ! command -v bat >/dev/null 2>&1; then
  ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
  echo "создана ссылка: ~/.local/bin/bat -> $(command -v batcat)"
fi
if command -v fdfind >/dev/null 2>&1 && ! command -v fd >/dev/null 2>&1; then
  ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
  echo "создана ссылка: ~/.local/bin/fd -> $(command -v fdfind)"
fi

if ! printf '%s' ":$PATH:" | grep -q ":$HOME/.local/bin:"; then
  echo
  echo "Внимание: ~/.local/bin отсутствует в PATH. Добавьте в ~/.bashrc:"
  echo '  export PATH="$HOME/.local/bin:$PATH"'
fi

echo
echo "Проверка:"
for tool in rg fd bat jq tree htop ncdu tmux; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "  OK   $tool"
  else
    echo "  нет  $tool"
  fi
done
