#!/usr/bin/env bash
# Запуск OpenCode через npx — без глобальной установки.
# Использование:
#   ./opencode-npx.sh           # запустить
#   ./opencode-npx.sh --help    # любые аргументы передаются OpenCode

set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  echo "Ошибка: Node.js не найден." >&2
  echo "Сначала выполните: ./install-nvm.sh && ./update-node.sh" >&2
  exit 1
fi

echo "==> Node.js $(node -v), npx $(npx --version)"
echo "==> Запускаю @opencode/cli@latest"
exec npx --yes @opencode/cli@latest "$@"
