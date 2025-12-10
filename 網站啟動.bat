@echo off
chcp 65001

cd /d "%~dp0"
echo 啟動網站中...

:: 設定 Flask 環境變數
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

:: 執行網站
python app.py 

:: 執行完後保持視窗開啟，方便看錯誤
echo.
echo 按任意鍵關閉...
pause >nul

