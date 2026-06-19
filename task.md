# 📝 Registro de Tareas: Boquerón Plan

## 🏗 In Progress / En Curso

- [/] **Fase 3: Construcción (`/build`)**
  - [/] Configuración de Entornos y Monorepo
  - [x] Configurar entorno virtual `backend/venv` e instalar dependencias.
  - [ ] Crear estructura de carpetas en `frontend/` (css, js, assets).

## ⏳ Pending / Pendientes (Backlog)

### 1. Backend (FastAPI - Python)
- [ ] Implementar la carga de variables de entorno y CORS en `main.py`.
- [ ] Implementar el servicio `ticketmaster.py` con filtros por Málaga, caché en memoria y mockups.
- [ ] Implementar el servicio de LLM `llm.py` con el System Prompt con acento de Málaga.
- [ ] Crear las rutas de API (`/api/chat` y `/api/events`).

### 2. Frontend (HTML5 / Vanilla JS)
- [ ] Configurar los estilos CSS en `frontend/css/styles.css` aplicando los tokens (blanco, azul, naranja).
- [ ] Crear la maqueta HTML principal `frontend/index.html`.
- [ ] Implementar el módulo `frontend/js/api.js` para conectar con FastAPI.
- [ ] Implementar el módulo `frontend/js/chat.js` para renderizar burbujas y tarjetas.
- [ ] Implementar el módulo `frontend/js/calendar.js` para renderizar el calendario y exportar `.ics`.
- [ ] Implementar el módulo `frontend/js/app.js` para orquestar filtros y estado global.

### 3. Pruebas y Verificación (`/test`)
- [ ] Escribir y ejecutar tests unitarios de backend con pytest.

### 4. Auditoría de Seguridad y Simplificación (`/code-simplify`)
- [ ] Verificar la ausencia de claves API expuestas e inyección de código.

### 5. Entrega y Agent Readiness (`/ship`)
- [ ] Crear archivos `robots.txt`, `llms.txt` y `auth.md`.
- [ ] Configurar metadatos en `.well-known/` (`agent.json`, `mcp.json`, `api-catalog`).
- [ ] Crear las guías de habilidades en `agent-skills/`.
- [ ] Generar los scripts de arranque/parada multiplataforma (`start.sh`, `start.cmd`, `stop.sh`, `stop.cmd`).
- [ ] Completar `walkthrough.md` y proponer versión/commit git.

---

## 🔄 Context Snapshot / Snapshot de Contexto

> **Last update / Última actualización:** 2026-06-19
> **Exact point / Punto exacto:** Backend venv configurado con dependencias. Frontend cambiado de React a Vanilla JS para adaptarse a la ausencia de Node.js.
> **Pending / Pendiente:** Iniciar el desarrollo del Backend.
> **Next step / Próximo paso:** Crear archivos backend/app/main.py and config.py.