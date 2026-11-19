#!/usr/bin/env bash
# Установка nvm (Node Version Manager).
# Использование: ./install-nvm.sh

set -euo pipefail

NVM_VERSION="${NVM_VERSION:-v0.41.0}"
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
INSTALL_URL="https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERSION}/install.sh"

echo "==> Проверка зависимостей"
if command -v curl >/dev/null 2>&1; then
  DOWNLOAD="curl -fsSL"
elif command -v wget >/dev/null 2>&1; then
  DOWNLOAD="wget -qO-"
else
  echo "Ошибка: нужен curl или wget." >&2
  echo "  Debian/Ubuntu: sudo apt install -y curl" >&2
  echo "  Fedora:        sudo dnf install -y curl" >&2
  echo "  Arch:          sudo pacman -S curl" >&2
  exit 1
fi

if [ -s "$NVM_DIR/nvm.sh" ]; then
  echo "==> nvm уже установлен: $NVM_DIR"
else
  echo "==> Устанавливаю nvm ${NVM_VERSION}"
  # shellcheck disable=SC2086
  $DOWNLOAD "$INSTALL_URL" | bash
fi

echo "==> Подхватываю nvm в текущей оболочке"
# shellcheck disable=SC1090
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
# shellcheck disable=SC1090
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

if command -v nvm >/dev/null 2>&1; then
  echo "==> Готово: nvm $(nvm --version)"
  echo
  echo "Откройте новый терминал (или выполните 'source ~/.bashrc'),"
  echo "затем запустите: ./update-node.sh"
else
  echo "Ошибка: nvm установлен, но не найден в оболочке." >&2
  echo "Откройте новый терминал и проверьте: command -v nvm" >&2
  exit 1
fi
