# Windows и WSL

Если в колледже на компьютерах Windows, а нужны Linux-команды — есть два пути.

## Путь 1: winget (быстро, без Linux)

Одна команда в PowerShell запускает [`scripts/bootstrap.ps1`](../scripts/bootstrap.ps1):

```powershell
irm https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.ps1 | iex
```

Скрипт ставит Git, VS Code, Node.js LTS, Windows Terminal, 7-Zip и Python.

Проверка после установки (открыть **новый** терминал):

```powershell
git --version
node -v
npm -v
code --version
python --version
```

Запуск OpenCode через npx:

```powershell
npx --yes @opencode/cli@latest
```

Ручная установка отдельных пакетов:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Microsoft.WindowsTerminal -e
winget install --id 7zip.7zip -e
winget install --id Python.Python.3.14 -e
```

Поиск актуального ID:

```powershell
winget search python
```

> `nvm` из [node-nvm-opencode.md](node-nvm-opencode.md) **не работает** в Windows: это bash-скрипт.
> Аналог для Windows — `nvm-windows` (`winget install CoreyButler.NVMforWindows`), но у него другой набор команд,
> либо используйте WSL.

## Путь 2: WSL (полноценный Linux внутри Windows)

### Установка

В PowerShell **от администратора**:

```powershell
wsl --install -d Ubuntu
```

Перезагрузка, затем Ubuntu попросит придумать логин и пароль (пароль не отображается при вводе).

Проверка:

```powershell
wsl --list --verbose
wsl --status
```

Вход в Linux:

```powershell
wsl
```

Или из меню «Пуск» → Ubuntu.

### Дальше — как на обычном Linux

Внутри Ubuntu работает всё из этого репозитория:

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.sh | bash
```

### Файлы

- Домашняя папка Linux: `\\wsl$\Ubuntu\home\<логин>` в Проводнике.
- Диск Windows доступен как `/mnt/c/Users/<логин>`.

> Проекты держите **внутри** Linux (`~/projects`), а не на `/mnt/c`: работа с файлами Windows из Linux медленная,
> а права и переводы строк ломают сборку.

### VS Code + WSL

```powershell
code .
```

Если VS Code запущен из папки Linux, он сам предложит подключиться к WSL (расширение **WSL**).
Дальше терминал, Python, Docker — всё внутри Linux.

### Docker в WSL

Docker Desktop умеет работать через WSL 2 (Settings → Resources → WSL Integration).
Альтернатива — установить Docker прямо в Ubuntu командами из [docker.md](docker.md).

## Частые проблемы

| Проблема | Решение |
|---|---|
| `wsl --install` требует прав | запустить PowerShell от администратора |
| WSL не запускается, ошибка про виртуализацию | включить в BIOS/Virtual Machine Platform в «Компоненты Windows» |
| `wsl --install` не находит Ubuntu | `wsl --list --online`, затем `wsl --install -d Ubuntu-24.04` |
| Не работает `code .` внутри WSL | установить VS Code в Windows, расширение WSL |
| `Permission denied` при записи на `/mnt/c` | писать в `~`, а не в папку Windows |
| Скрипты падают с `\r` | `sed -i 's/\r$//' script.sh` или `dos2unix script.sh` |

## PowerShell: полезное

```powershell
Get-ChildItem              # ls
Set-Location путь          # cd
Get-Content файл           # cat
Remove-Item файл           # rm
Get-Command node           # which
$env:PATH                  # переменная PATH
Get-Help команда -Examples
```

Алиасы (`$PROFILE`):

```powershell
function ll { Get-ChildItem -Force }
function gs { git status }
```
