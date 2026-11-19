#!/usr/bin/env bash
# Всё сразу: установка nvm + Node.js LTS + npm, затем подсказка по OpenCode.
# Использование: ./setup-all.sh

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo " 1/2  Установка nvm"
echo "========================================"
bash "$DIR/install-nvm.sh"

echo
echo "========================================"
echo " 2/2  Обновление Node.js до LTS"
echo "========================================"
bash "$DIR/update-node.sh"

echo
echo "========================================"
echo " Готово"
echo "========================================"
echo "Запуск OpenCode без установки:"
echo "  npx --yes @opencode/cli@latest"
echo
echo "Запуск через скрипт:"
echo "  ./opencode-npx.sh"
echo
echo "Постоянная установка:"
echo "  npm install -g @opencode/cli"
