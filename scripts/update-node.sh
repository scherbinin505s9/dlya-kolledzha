#!/usr/bin/env bash
# Обновление Node.js через nvm.
# Использование:
#   ./update-node.sh          # последняя LTS-версия
#   ./update-node.sh lts      # то же самое
#   ./update-node.sh node     # последняя версия (не LTS)
#   ./update-node.sh 26       # конкретная мажорная версия
#   ./update-node.sh 24.22.3  # конкретная точная версия

set -euo pipefail

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# shellcheck disable=SC1090
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

if ! command -v nvm >/dev/null 2>&1; then
  echo "Ошибка: nvm не найден. Сначала запустите ./install-nvm.sh" >&2
  exit 1
fi

TARGET="${1:-lts}"
OLD="$(nvm current 2>/dev/null || echo none)"

echo "==> Текущая версия Node.js: ${OLD}"

case "$TARGET" in
  lts|--lts) nvm install --lts ;;
  *)         nvm install "$TARGET" ;;
esac

NEW="$(nvm current)"

if [ "$OLD" != "none" ] && [ "$OLD" != "system" ] && [ "$OLD" != "$NEW" ]; then
  echo "==> Переношу глобальные пакеты: ${OLD} -> ${NEW}"
  nvm reinstall-packages-from="$OLD" || \
    echo "    Часть пакетов не перенеслась — установите их вручную: npm install -g <пакет>"
fi

case "$TARGET" in
  lts|--lts) nvm alias default 'lts/*' ;;
  node)      nvm alias default 'node' ;;
  *)         nvm alias default "$NEW" ;;
esac

nvm use "$NEW" >/dev/null

echo "==> Обновляю npm"
npm install -g npm@latest

echo
echo "==> Готово"
echo "    node: $(node -v)"
echo "    npm:  $(npm -v)"
echo "    путь: $(command -v node)"
echo
echo "Откройте новый терминал, чтобы версия применилась везде."
