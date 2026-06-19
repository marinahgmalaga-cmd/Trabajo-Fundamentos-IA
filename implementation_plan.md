---
dependencies:
  frontend:
    - none (Vanilla HTML/CSS/JS nativo)
  backend:
    - fastapi
    - uvicorn
    - openai
    - requests
    - python-dotenv
    - pydantic
risks:
  - Exposición de claves de API de OpenAI o Ticketmaster.
  - El LLM genera respuestas que no siguen el formato JSON esperado para tarjetas dinámicas.
  - Caída o agotamiento de cuotas de la API de Ticketmaster.
rollback_strategy:
  - En caso de error crítico, revertir al commit inicial de bootstrap con `git reset --hard a863282`.
---

# Plan de Implementación: Boquerón Plan

Plan para construir una aplicación web interactiva que permite a los usuarios buscar eventos en Málaga a través de un chat con un guía local de IA ("El Boquerón"), filtrar planes manualmente y exportarlos en formato `.ics` para su calendario personal.

## User Review Required

> [!IMPORTANT]
> **Modelo y Claves de API:** Para que el backend funcione, necesitaremos configurar variables de entorno para la API de OpenAI/Gemini y la de Ticketmaster. Deberás crear un archivo `.env` en la carpeta `backend/` con estas claves.
> **Generación de .ics en Frontend:** La exportación del calendario se realizará de forma puramente cliente para mayor simplicidad y privacidad, evitando procesos de OAuth de Google o Outlook.

## Proposed Changes

### [Backend]
Servidor FastAPI en Python para gestionar las llamadas a la API de LLM (OpenAI) y API de Ticketmaster de forma segura.

#### [NEW] [main.py](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/app/main.py)
- Punto de entrada. Configuración de FastAPI y middleware CORS para permitir peticiones desde el frontend.

#### [NEW] [config.py](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/app/config.py)
- Configuración de variables de entorno con `python-dotenv` para cargar API Keys de OpenAI y Ticketmaster.

#### [NEW] [llm.py](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/app/services/llm.py)
- Servicio que interactúa con la API del LLM. Incluye el System Prompt de "El Boquerón" con acento malagueño y reglas estrictas de filtrado de eventos.

#### [NEW] [ticketmaster.py](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/app/services/ticketmaster.py)
- Consultas a Ticketmaster filtradas por Málaga (lat/long o ciudad). Caché interna en memoria y fallback a datos mockup.

#### [NEW] [routes](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/app/routes)
- Endpoints `/api/chat` y `/api/events` para servir al frontend.

#### [NEW] [requirements.txt](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/backend/requirements.txt)
- Definición de dependencias de Python.

---

### [Frontend]
Cliente en HTML/CSS/JS nativo (ES6 Modules) para renderizar la interfaz limpia, fresca y mediterránea, sin necesidad de compilar ni instalar Node.js.

#### [NEW] [index.html](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/index.html)
- Estructura HTML del sitio web: cabecera, contenedor de chat y panel de filtros/calendario lateral.

#### [NEW] [styles.css](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/css/styles.css)
- Hoja de estilos principal con los tokens de diseño (fondo blanco, azul mediterráneo, naranja suave) y efectos de animación.

#### [NEW] [app.js](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/js/app.js)
- Orquestador de la UI. Gestiona el estado de los filtros y coordina los demás módulos de JS.

#### [NEW] [chat.js](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/js/chat.js)
- Módulo del chat: control de burbujas, inserción de tarjetas y animación de "El Boquerón escribiendo...".

#### [NEW] [calendar.js](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/js/calendar.js)
- Módulo de calendario: renderizado del calendario lateral e implementación de la exportación a archivo `.ics` nativo en Javascript.

#### [NEW] [api.js](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/frontend/js/api.js)
- Módulo cliente HTTP de conexión con el backend de FastAPI.

---

### [Agent Readiness & Discovery]
Archivos de autodescubrimiento y SEO para agentes inteligentes externos.

#### [NEW] [robots.txt](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/robots.txt)
- Fichero robots.txt con `Content-Signal` especial.

#### [NEW] [llms.txt](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/llms.txt)
- Mapa de navegación de IA en Markdown.

#### [NEW] [auth.md](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/auth.md)
- Instrucciones de acceso para bots y agentes de chat.

#### [NEW] [.well-known](file:///Users/marinaheezemans/Desktop/Proyecto%2019junio/.well-known)
- Catálogo de APIs, tarjetas de agente (`agent.json`) y MCP (`mcp.json`).

---

## Verification Plan

### Automated Tests
- Pruebas unitarias de respuesta del LLM y parseo de eventos de Ticketmaster en backend usando pytest.

### Manual Verification
- Comprobar la interactividad del chat y simular respuestas con modismos de Málaga.
- Hacer clic en "Agendar Plan" y verificar que el archivo `.ics` descargado se puede abrir en Google Calendar con el título, fecha y ubicación correctos.
- Ejecutar el servidor web local con `python3 -m http.server` en la carpeta frontend y verificar la correcta carga sin errores de consola.
