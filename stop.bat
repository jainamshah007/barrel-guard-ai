@echo off
:: =============================================================
:: BARREL-GUARD AI — Foreign Object Detection Platform
:: Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
:: Unauthorized copying, modification, or distribution of
:: this file, via any medium, is strictly prohibited.
:: =============================================================

title BARREL-GUARD AI — Shutdown
color 0C

echo.
echo  ============================================
echo   BARREL-GUARD AI — Stopping All Services
echo   Copyright (c) 2024 Jainam K Shah
echo   All Rights Reserved.
echo  ============================================
echo.

docker-compose down

echo.
echo  All services stopped successfully.
echo.
pause
