#!/usr/bin/env bash
# Установка .NET SDK без root — в $HOME/.dotnet.
# Использование: ./install-dotnet.sh [версия]
# Пример:        ./install-dotnet.sh 8.0

set -euo pipefail

CHANNEL="${1:-${DOTNET_CHANNEL:-10.0}}"
DOTNET_DIR="${DOTNET_DIR:-$HOME/.dotnet}"
INSTALL_URL="https://dot.net/v1/dotnet-install.sh"

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

TMP_SCRIPT="$(mktemp)"
trap 'rm -f "$TMP_SCRIPT"' EXIT

echo "==> Скачиваю установщик .NET"
# shellcheck disable=SC2086
$DOWNLOAD "$INSTALL_URL" >"$TMP_SCRIPT"
chmod +x "$TMP_SCRIPT"

echo "==> Ставлю .NET SDK ${CHANNEL} в ${DOTNET_DIR}"
"$TMP_SCRIPT" --channel "$CHANNEL" --install-dir "$DOTNET_DIR"

echo "==> Прописываю PATH в ~/.bashrc и ~/.zshrc"
PATH_LINE='export PATH="$HOME/.dotnet:$PATH"'
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  # shellcheck disable=SC2016
  if [ -f "$rc" ] && ! grep -qF 'PATH="$HOME/.dotnet:$PATH"' "$rc"; then
    printf '\n# .NET SDK\n%s\n' "$PATH_LINE" >>"$rc"
    echo "    добавлено в $rc"
  fi
done

export PATH="$DOTNET_DIR:$PATH"

if command -v dotnet >/dev/null 2>&1; then
  echo "==> Готово: dotnet $(dotnet --version)"
  echo
  echo "Откройте новый терминал, затем проверьте:"
  echo "  dotnet --list-sdks"
else
  echo "Ошибка: dotnet установлен, но не найден в PATH." >&2
  echo "Выполните: export PATH=\"$DOTNET_DIR:\$PATH\"" >&2
  exit 1
fi
