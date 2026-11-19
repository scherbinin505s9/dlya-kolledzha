#!/usr/bin/env pwsh
# Настройка свежей Windows-машины через winget.
#
#   powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1
#   irm https://raw.githubusercontent.com/scherbinin505s9/dlya-kolledzha/main/scripts/bootstrap.ps1 | iex
#
# Что ставит: Git, VS Code, Node.js LTS, Windows Terminal, 7-Zip, Python 3.14.
# Параметры:
#   -SkipPython   не ставить Python
#   -SkipVSCode   не ставить VS Code
#   -DryRun       только показать, что будет установлено

[CmdletBinding()]
param(
    [switch]$SkipPython,
    [switch]$SkipVSCode,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Step($text) {
    Write-Host ""
    Write-Host "===== $text =====" -ForegroundColor Cyan
}

function Test-Winget {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget не найден. Обновите Windows или установите App Installer из Microsoft Store."
    }
}

function Install-Package($id, $name) {
    $installed = winget list --id $id -e --source winget 2>$null | Select-String -SimpleMatch $id
    if ($installed) {
        Write-Host "уже установлено: $name ($id)" -ForegroundColor DarkGray
        return
    }
    if ($DryRun) {
        Write-Host "будет установлено: $name ($id)" -ForegroundColor Yellow
        return
    }
    Write-Host "ставлю: $name ($id)" -ForegroundColor Green
    winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
}

Write-Step "Проверка winget"
Test-Winget
winget --version

$packages = @(
    @{ id = 'Git.Git';                    name = 'Git' },
    @{ id = 'OpenJS.NodeJS.LTS';          name = 'Node.js LTS' },
    @{ id = 'Microsoft.WindowsTerminal';  name = 'Windows Terminal' },
    @{ id = '7zip.7zip';                  name = '7-Zip' }
)

if (-not $SkipVSCode) {
    $packages += @{ id = 'Microsoft.VisualStudioCode'; name = 'Visual Studio Code' }
}

if (-not $SkipPython) {
    $packages += @{ id = 'Python.Python.3.14'; name = 'Python 3.14' }
}

foreach ($pkg in $packages) {
    Write-Step $pkg.name
    Install-Package $pkg.id $pkg.name
}

Write-Step "Готово"
Write-Host "Откройте НОВЫЙ терминал (PATH обновляется только при старте) и проверьте:" -ForegroundColor Cyan
Write-Host "  git --version"
Write-Host "  node -v"
Write-Host "  npm -v"
Write-Host "  code --version"
if (-not $SkipPython) { Write-Host "  python --version" }
Write-Host ""
Write-Host "OpenCode без установки:" -ForegroundColor Cyan
Write-Host "  npx --yes @opencode/cli@latest"
Write-Host ""
Write-Host "Нужен полноценный Linux? Установите WSL:" -ForegroundColor Cyan
Write-Host "  wsl --install -d Ubuntu"
