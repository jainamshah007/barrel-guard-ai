@echo off
:: =============================================================
:: BARREL-GUARD AI — Foreign Object Detection Platform
:: Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
:: Unauthorized copying, modification, or distribution of
:: this file, via any medium, is strictly prohibited.
:: =============================================================

title BARREL-GUARD AI — Startup
color 0A

echo.
echo  ============================================
echo   BARREL-GUARD AI — Foreign Object Detection
echo   Copyright (c) 2024 Jainam K Shah
echo   All Rights Reserved.
echo  ============================================
echo.
echo  Starting all services via Docker...
echo.

docker-compose up --build -d

echo.
echo  All services started successfully!
echo  Opening dashboard...
echo.

timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo  Dashboard is running at: http://localhost:3000
echo  API is running at:       http://localhost:8000
echo  API Docs at:             http://localhost:8000/docs
echo.
pause
