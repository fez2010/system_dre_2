# Check for Administrator privileges
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "Please run this script as Administrator."
    exit
}

Write-Host "--- Starting Windows Setup ---" -ForegroundColor Cyan

# 1. Run Library Setup (Replacement for setup/ubuntu/libs.sh)
Write-Host "Installing Libraries..." -ForegroundColor Yellow
& ".\setup\windows\libs.ps1"

# 2. Run Font Setup (Replacement for setup/ubuntu/font_setup.sh)
Write-Host "Installing Fonts..." -ForegroundColor Yellow
& ".\setup\windows\font_setup.ps1"

Write-Host "--- Setup Complete! ---" -ForegroundColor Green