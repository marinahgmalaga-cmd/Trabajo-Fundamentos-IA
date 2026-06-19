# 🏗 Arquitectura Técnica: Boquerón Plan

> **Fase:** `/plan` (Planificación Técnica)
> **Estado:** Validado
> **Última Revisión:** 2026-06-19

---

## 🛠 Stack Tecnológico

| Capa | Tecnología | Justificación |
| --- | --- | --- |
| **Frontend** | HTML5 / Vanilla JavaScript (ES6 Modules) | Rápida reactividad, sin compilación, compatible con cualquier servidor local y fácil de portar sin Node.js. |
| **Estilos** | CSS Vanilla | Máxima flexibilidad, transiciones suaves y control total de los tokens de color mediterráneos. |
| **Backend** | Python 3.11+ (FastAPI) | Conectividad ideal con librerías de IA, asincronía nativa y alto rendimiento para proxies de APIs de terceros. |
| **Sistema de Diseño** | CSS/UI | Estilo limpio, fresco y mediterráneo con fondo blanco predominante, toques de azul mediterráneo en cabeceras y elementos interactivos, y acentos puntuales de naranja cálido para precios y alertas. Ver detalles en `docs/DESIGN.md`. |
| **Persistencia** | LocalStorage (Navegador) | Almacenamiento local en cliente del historial de chat y de los planes agendados. Evita la sobrecarga de una base de datos para el MVP académico. |
| **Integración IA** | OpenAI API / Gemini API | Utilización de modelos rápidos y de bajo coste (GPT-4o-mini o Gemini 1.5 Flash) configurados con personalidad local. |
| **Calendario** | Exportación Universal `.ics` | Generación en cliente de archivos de calendario universal. Sin fricción ni necesidad de OAuth complejo. |
| **Pruebas** | pytest (Backend) | Ecosistema moderno, rápido y compatible. |

---

## 📂 Estructura de Directorios

```text
/
├── backend/                  # Servidor Python con FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Entrada y configuración del servidor
│   │   ├── config.py         # Carga de secretos y variables de entorno (.env)
│   │   ├── routes/
│   │   │   ├── chat.py       # Endpoint para enviar mensajes al bot
│   │   │   └── events.py     # Endpoint para consultar eventos de Málaga
│   │   └── services/
│   │       ├── llm.py        # Integración con OpenAI/Gemini y System Prompt
│   │       └── ticketmaster.py # Conexión y consulta a la API de Ticketmaster
│   ├── requirements.txt      # Dependencias (fastapi, uvicorn, openai, requests, etc.)
│   └── tests/                # Pruebas unitarias de endpoints y prompts
├── frontend/                 # Interfaz de usuario con HTML/CSS/JS nativo
│   ├── index.html            # Estructura HTML de la página web
│   ├── css/
│   │   └── styles.css        # Estilos generales y tokens de diseño (DESIGN.md)
│   ├── js/
│   │   ├── app.js            # Lógica y estado principal de la aplicación
│   │   ├── chat.js           # Renderizado y lógica de conversación con El Boquerón
│   │   ├── calendar.js       # Lógica del calendario y exportación de archivos .ics
│   │   └── api.js            # Conectividad con la API del backend FastAPI
│   └── assets/               # Imágenes, iconos y avatar
├── docs/                     # Documentación de Ingeniería SDD
├── start.sh / start.cmd      # Scripts de arranque multiplataforma
├── stop.sh / stop.cmd        # Scripts de parada multiplataforma
└── [config files]            # project.config.md, memory.md, task.md
```

---

## 🔑 Decisiones Técnicas Clave

### 1. Exportación `.ics` vs OAuth de Calendarios
- **Decisión:** Se generarán archivos estándar `.ics` del lado del cliente.
- **Justificación:** Integrar OAuth para Google Calendar o Microsoft Outlook añade una alta complejidad en la gestión de tokens, consentimiento de seguridad e infraestructura en la nube. Un archivo `.ics` es universal, funciona al instante en cualquier dispositivo (móvil o PC) y se importa en un solo toque, cumpliendo la especificación con coste cero de desarrollo técnico y de seguridad.

### 2. Personalidad de la IA ("El Boquerón")
- **Decisión:** El backend enviará las consultas de chat a OpenAI/Gemini inyectando un **System Prompt** robusto.
- **System Prompt Base:**
  > "Eres 'El Boquerón', un guía local de Málaga. Tienes un acento malagueño marcado y usas expresiones locales como 'pechá', 'boquerón', 'perita', 'guiri', 'alohe' o 'cusha'. Tu objetivo es recomendar planes reales de conciertos, fútbol o eventos en Málaga con simpatía. Sé conciso, alegre y mantén siempre el hilo sobre eventos de la provincia. Si te preguntan algo ajeno, reconduce con gracia al terreno local."

### 3. Caché de Eventos y Mockups
- **Decisión:** Guardar en caché local en memoria (FastAPI memory cache) los resultados de Ticketmaster por 1 hora.
- **Justificación:** La API de desarrollo de Ticketmaster tiene límites estrictos. Cachear las búsquedas por zona e interés optimiza el consumo de la API y reduce la latencia del chat. Si las APIs fallan o no hay conexión, se servirá un set predefinido de eventos populares mockeados de Málaga (partidos del Málaga CF, conciertos en la Sala Trinchera, festivales en Marenostrum Fuengirola).

---

## 🤖 Agent Harness (Arnés del Agente)

### 1. Gestión de Contexto (Context Engineering)
- **Contexto Estático:** Ficheros `GEMINI.md`, `ANTIGRAVITY.md` y `memory.md` en el arranque.
- **Contexto Dinámico / Skills:** Definición de habilidades para agentes en el directorio `.well-known/agent-skills/` para que IAs externas comprendan cómo consumir nuestra recomendación de eventos de Málaga.

### 2. Guardrails Deterministas de Seguridad
- **Filtros de Código:** Script pre-commit que audita claves API expuestas (`gitleaks` o regex de llaves OpenAI/Gemini en ficheros de configuración).
- **Entorno Aislado:** Desarrollo en entorno virtual de Python (`venv/`) para aislar dependencias del sistema.

### 3. Interfaz Externa para Agentes (Agent Readiness)
*Este proyecto web está diseñado para ser Agent-Ready (Yes):*
- **Autodescubrimiento**: Inyección de cabeceras `Link` HTTP en el hosting o servidor apuntando a `/llms.txt`, `.well-known/api-catalog` y `.well-known/agent.json`.
- **Tarjetas de Agente y MCP**:
  - `.well-known/agent.json`: Fichero que describe las capacidades de recomendación de eventos de Málaga de este sitio.
  - `.well-known/mcp.json`: Configuración para conectar este proyecto como un servidor MCP local, permitiendo a otros agentes llamar a la función de búsqueda de eventos.
- **Negociación de Markdown**: El backend FastAPI responderá con texto estructurado en Markdown cuando reciba el header `Accept: text/markdown` en `/api/events` o `/api/chat`.
