@echo off
chcp 65001 >nul
cd /d "%~dp0"
title TravelSnap HU05 HU15 HU06
if not exist "server.py" (
  echo ERROR: No se encuentra server.py en esta carpeta.
  pause
  exit /b 1
)
echo Iniciando TravelSnap desde: %CD%
echo Abre http://localhost:8000 en el navegador cuando aparezca el mensaje de servidor activo.
echo Si el puerto 8000 esta ocupado, cierra el servidor anterior con Ctrl+C.
echo.
python server.py
if errorlevel 1 (
  echo.
  echo No se pudo iniciar TravelSnap. Revisa el mensaje anterior.
  pause
)
