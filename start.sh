#!/bin/bash
# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================
# start.sh — Arrancar backend (FastAPI) y frontend (HTTP estático)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🐟 Boquerones a la calle — Iniciando..."
echo "================================="

# Arrancar el backend FastAPI en segundo plano
echo "▶ Backend: iniciando FastAPI en http://127.0.0.1:8000"
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
nohup venv/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/boqueron_backend.log 2>&1 &
BACKEND_PID=$!
echo "  PID del backend: $BACKEND_PID"
echo "$BACKEND_PID" > /tmp/boqueron_backend.pid
cd "$SCRIPT_DIR"

# Esperar brevemente para que arranque el backend
sleep 2

# Arrancar el servidor de frontend en segundo plano
echo "▶ Frontend: iniciando servidor estático en http://127.0.0.1:8080"
cd "$SCRIPT_DIR/frontend"
nohup python3 -m http.server 8080 > /tmp/boqueron_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  PID del frontend: $FRONTEND_PID"
echo "$FRONTEND_PID" > /tmp/boqueron_frontend.pid
cd "$SCRIPT_DIR"

echo "================================="
echo "✅ ¡Todo listo, boquerón!"
echo "   🌐 Frontend → http://127.0.0.1:8080"
echo "   ⚙️  Backend API → http://127.0.0.1:8000"
echo "   📖 API Docs → http://127.0.0.1:8000/docs"
echo ""
echo "Para parar los servidores, ejecuta: ./stop.sh"
