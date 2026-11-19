#!/usr/bin/env bash
# Диагностика окружения: что установлено и откуда запускается.
# Использование: ./check-env.sh

set -uo pipefail

line() { printf '%s\n' "----------------------------------------"; }

line
echo " Система"
line
if [ -r /etc/os-release ]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  echo "Дистрибутив: ${PRETTY_NAME:-неизвестен}"
else
  echo "Дистрибутив: $(uname -s)"
fi
echo "Ядро:        $(uname -r)"
echo "Архитектура: $(uname -m)"
echo "Оболочка:    ${SHELL:-неизвестна}"

line
echo " Node.js и npm"
line
if command -v node >/dev/null 2>&1; then
  echo "node:  $(node -v)  ($(command -v node))"
else
  echo "node:  не установлен"
fi
if command -v npm >/dev/null 2>&1; then
  echo "npm:   $(npm -v)  ($(command -v npm))"
else
  echo "npm:   не установлен"
fi

line
echo " nvm"
line
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1090
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" >/dev/null 2>&1

if command -v nvm >/dev/null 2>&1; then
  echo "версия:   $(nvm --version)"
  echo "каталог:  $NVM_DIR"
  echo "текущая:  $(nvm current)"
  echo "версии:   $(nvm ls | tr '\n' ' ')"
  echo "default:  $(nvm alias default 2>/dev/null | tail -n 1)"
else
  echo "nvm не установлен (или не подгружен в этой оболочке)"
fi

line
echo " OpenCode"
line
if command -v opencode >/dev/null 2>&1; then
  echo "opencode: $(command -v opencode)"
else
  echo "opencode: не установлен глобально"
  echo "запуск без установки: npx --yes @opencode/cli@latest"
fi

line
echo " npm config"
line
if command -v npm >/dev/null 2>&1; then
  echo "registry: $(npm config get registry)"
  echo "prefix:   $(npm config get prefix)"
  echo "глобальные пакеты:"
  npm ls -g --depth=0 2>/dev/null | sed 's/^/  /'
fi

line
echo " PATH"
line
echo "${PATH}" | tr ':' '\n' | sed 's/^/  /'
