# 📝 Registro de Tareas: Boquerones a la calle

## ✅ Completed / Completadas

- [x] **Fase 2: Planificación y Aprobación**
- [x] **Fase 3: Construcción (`/build`)**
  - [x] Configurar entorno virtual `backend/venv` e instalar dependencias (FastAPI, uvicorn, openai, requests, pydantic).
  - [x] Crear estructura de carpetas en `frontend/` (css, js, assets).
  - [x] Backend: `config.py`, `main.py`, `services/ticketmaster.py`, `services/llm.py`, `routes/chat.py`, `routes/events.py`.
  - [x] Frontend: `index.html`, `css/styles.css`, `js/api.js`, `js/chat.js`, `js/calendar.js`, `js/app.js`.
  - [x] Scripts multiplataforma: `start.sh`, `stop.sh`, `start.cmd`, `stop.cmd`.
  - [x] Git commit `cf8294e` — "feat: implementación inicial de Boquerones a la calle v0.1.0"

## ⏳ Pending / Pendientes (Backlog)

### 1. Pruebas y Verificación (`/test`)
- [ ] Escribir y ejecutar tests unitarios de backend con pytest.

### 2. Auditoría de Seguridad y Simplificación (`/code-simplify`)
- [ ] Verificar la ausencia de claves API expuestas e inyección de código.

### 3. Entrega y Agent Readiness (`/ship`)
- [ ] Crear archivos `robots.txt`, `llms.txt` y `auth.md`.
- [ ] Configurar metadatos en `.well-known/` (`agent.json`, `mcp.json`, `api-catalog`).
- [ ] Crear las guías de habilidades en `agent-skills/`.
- [ ] Completar `walkthrough.md` y proponer versión/commit git.

---

## 🔄 Context Snapshot / Snapshot de Contexto

> **Last update / Última actualización:** 2026-06-19
> **Exact point / Punto exacto:** v0.1.0 construida y commiteada (commit cf8294e). Backend FastAPI + Frontend HTML/JS operativos y verificados con curl.
> **Pending / Pendiente:** Tests automatizados (pytest), code-simplify y fase /ship con Agent Readiness.
> **Next step / Próximo paso:** Ejecutar `./start.sh` y verificar la web en http://127.0.0.1:8080.