@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"

echo ============================================
echo   Genshin Checkin - QR Login (get Cookie)
echo ============================================
echo.
echo [1/2] checking dependencies...
python -m pip install -q requests qrcode pillow

echo [2/2] starting QR login...
echo.
python qr_login.py

echo.
echo ============================================
echo  Copy the COOKIE line above, then close.
echo ============================================
pause >nul
