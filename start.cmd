@echo off
:: =============================================================================
:: Proyecto 19junio — Sitio web interactivo
:: Copyright (c) 2026 Marina Heezemans
:: Licensed under the MIT License. See LICENSE for details.
:: Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
:: =============================================================================
:: start.cmd — Arrancar backend (FastAPI) y frontend (HTTP estático)

echo Boquerones a la calle - Iniciando...
echo =================================

:: Arrancar backend FastAPI
echo Arrancando backend en http://127.0.0.1:8000
cd backend
start "Boqueron-Backend" cmd /c "venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
cd ..

:: Esperar a que arranque el backend
timeout /t 3 /nobreak >nul

:: Arrancar frontend
echo Arrancando frontend en http://127.0.0.1:8080
cd frontend
start "Boqueron-Frontend" cmd /c "python -m http.server 8080"
cd ..

echo =================================
echo Todo listo!
echo   Web: http://127.0.0.1:8080
echo   API: http://127.0.0.1:8000
echo   Docs: http://127.0.0.1:8000/docs
echo Para parar: ejecuta stop.cmd
