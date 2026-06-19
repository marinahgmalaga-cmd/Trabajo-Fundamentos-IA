#!/bin/bash
# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================
# stop.sh — Detener backend y frontend

echo "🛑 Boquerón Plan — Deteniendo servidores..."

if [ -f /tmp/boqueron_backend.pid ]; then
  BACKEND_PID=$(cat /tmp/boqueron_backend.pid)
  kill "$BACKEND_PID" 2>/dev/null && echo "  ✅ Backend detenido (PID $BACKEND_PID)" || echo "  ⚠️  Backend ya estaba detenido"
  rm -f /tmp/boqueron_backend.pid
fi

if [ -f /tmp/boqueron_frontend.pid ]; then
  FRONTEND_PID=$(cat /tmp/boqueron_frontend.pid)
  kill "$FRONTEND_PID" 2>/dev/null && echo "  ✅ Frontend detenido (PID $FRONTEND_PID)" || echo "  ⚠️  Frontend ya estaba detenido"
  rm -f /tmp/boqueron_frontend.pid
fi

echo "================================="
echo "¡Hasta luego, boquerón! 👋"
