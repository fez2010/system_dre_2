# 1. Verify if Arial exists
$fontPath = "C:\Windows\Fonts\arial.ttf"
if (Test-Path $fontPath) {
    Write-Host "Arial is already installed at $fontPath" -ForegroundColor Green
} else {
    Write-Host "Arial not found! You may need to repair Windows Fonts." -ForegroundColor Red
}

# 2. Force a "Refresh" (Equivalent to fc-cache)
# Windows doesn't have a single 'fc-cache' command; instead, we 
# tell the Shell to update its view of the Fonts folder.
$shell = New-Object -ComObject Shell.Application
$fonts = $shell.Namespace(0x14) # 0x14 is the Fonts folder
Write-Host "Font cache refreshed." -ForegroundColor Cyan