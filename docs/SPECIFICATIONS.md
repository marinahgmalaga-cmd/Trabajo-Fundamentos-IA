# 📋 Especificaciones: Boquerones a la calle (Guía Local IA de Málaga)

> **Fase:** `/spec` (Especificación)
> **Estado:** Validado
> **Última Revisión:** 2026-06-19
> **Proyecto:** Boquerones a la calle

---

## 🎯 1. Contexto y Objetivos
*Basado en la filosofía de "entender el problema antes de proponer la solución".*

- **Problema:** La dispersión de información sobre eventos (conciertos, partidos de fútbol, festivales, teatro) en Málaga dificulta encontrar planes de manera rápida. Además, existe fricción al tener que agendar manualmente los planes encontrados en el calendario personal del usuario (Google, Apple, Outlook).
- **Objetivo (Éxito):** Crear una web interactiva donde los usuarios puedan chatear con un asistente de IA con la personalidad y el acento de un guía local malagueño ("Boquerón"). La IA sugerirá planes personalizados según presupuesto, fecha y gustos, y permitirá añadirlos directamente al calendario del usuario mediante archivos `.ics` generados al instante, visualizándolos en un calendario interno de la web.

## 👥 2. Usuarios y Escenarios
*Identifica para quién construimos y en qué situaciones usarán el sistema.*

- **Perfil de Usuario:**
  - Turistas que visitan Málaga y buscan planes auténticos.
  - Residentes locales (malagueños) que quieren descubrir conciertos, partidos de fútbol del Málaga CF o festivales de fin de semana.
  - Estudiantes universitarios con presupuestos limitados.
- **Escenarios Clave:**
  - *Escenario A (Chat conversacional):* Un usuario le dice al bot: "Quiero ir a un concierto este sábado con mis amigos, tenemos unos 20€ de presupuesto cada uno". El bot responde con salero malagueño y le muestra tarjetas de conciertos que coinciden con esos criterios.
  - *Escenario B (Filtro rápido):* Un usuario que prefiere no escribir utiliza el panel lateral de filtros para seleccionar "Fútbol" y la fecha de "Este fin de semana", mostrando inmediatamente el próximo partido en La Rosaleda.
  - *Escenario C (Agendar en calendario):* El usuario ve un plan que le gusta ("Concierto de rock en el Wizink... o en la Sala Trinchera de Málaga"). Hace clic en "Agendar", se genera un archivo `.ics` y se descarga para añadirse a su Google Calendar en un toque. El evento aparece en la vista de calendario integrada en la propia web.

## ✨ 3. Funcionalidades Principales (Requisitos)
*El "Qué" del sistema. Estas tareas se trasladarán luego a `task.md`.*

- [ ] **Chat Conversacional con IA (Personaje Malagueño):**
  - Interfaz de chat de burbujas fluidas.
  - Persona: Un malagueño dicharachero y acogedor que utiliza expresiones locales ("boquerón", "pechá", "guiri", "alohe", "perita").
  - Envío y recepción de mensajes, mostrando un indicador de "escribiendo...".
- [ ] **Tarjetas de Eventos Dinámicas:**
  - Generación de tarjetas basadas en la conversación y la API de eventos.
  - Campos: Imagen del evento, Título, Fecha y Hora, Precio (o indicativo de Gratis), Ubicación e Enlace de compra si aplica.
- [ ] **Filtros Rápidos:**
  - Selector de categoría (Música/Conciertos, Deportes, Festivales, Culturales).
  - Rango de precios y selector de fechas (Hoy, Fin de semana, Próxima semana).
- [ ] **Exportación a Calendario (.ics universal):**
  - Botón "Agendar" en cada tarjeta.
  - Generación dinámica al vuelo de un archivo `.ics` compatible con Google Calendar, Apple Calendar y Outlook.
- [ ] **Vista de Calendario Interno:**
  - Un componente de calendario (vista mensual/semanal) que muestra los planes que el usuario ha decidido agendar en la sesión actual.
- [ ] **Mapa de Eventos (Opcional/Futuro):**
  - Visualización geográfica de los eventos recomendados usando Leaflet/OpenStreetMap.
- [ ] **Página "Sobre el personaje":**
  - Breve sección dedicada a explicar quién es "El Boquerón" y la motivación del proyecto académico de IA.

### 3.1. Agent Readiness Checklist (Proyectos Web)
*Configuración de descubrimiento para agentes inteligentes (Web Agent Readiness):*
- [ ] **robots.txt**: Configurar en la raíz con directivas `Content-Signal: ai-train=no, search=yes, ai-input=yes` y enlace al sitemap de IA.
- [ ] **llms.txt**: Crear mapa de contenidos del proyecto en Markdown para facilitar la lectura del asistente y la navegación agéntica.
- [ ] **auth.md**: Describir las instrucciones de acceso para bots y el simulador de chat de eventos.
- [ ] **Metadatos en `.well-known/`**:
  - `api-catalog`: Catálogo RFC 9727 con endpoints para bots.
  - `oauth-protected-resource` y `oauth-authorization-server`: Marcadores de endpoints.
  - `http-message-signatures-directory`: Directorio de firma para llamadas seguras.
- [ ] **Agent & MCP Cards**:
  - `.well-known/agent.json`: Declaración de la identidad y capacidades del agente local.
  - `.well-known/mcp.json`: Tarjeta de conexión del servidor MCP si un agente desea interactuar con nuestra API de eventos de Málaga.
- [ ] **agent-skills/**:
  - `index.json`: Índice de habilidades que el agente externo puede consultar.
  - `get-events.md` / `recommend-plans.md`: Guías Markdown de habilidades que describen cómo interactuar y llamar a nuestras herramientas de recomendación.
- [ ] **Negociación de Markdown**: Configurar el backend para retornar la versión Markdown cuando la cabecera `Accept: text/markdown` esté presente en la consulta.

## 🏗️ 4. Propuesta de Solución Técnica (Resumen)
*Enlace directo con `ARCHITECTURE.md`.*

- **Enfoque:** Monorepo con frontend en **React (Vite)** y backend en **Python (FastAPI)**. React manejará el estado dinámico (mensajes, tarjetas de eventos, calendario) y FastAPI servirá como puente seguro con las APIs de IA (OpenAI GPT o Anthropic Claude) y APIs de eventos, protegiendo las API Keys.
- **APIs y Datos:**
  - **Ticketmaster API (Discovery):** Para conciertos, festivales y eventos en Málaga.
  - **Football-data.org (u otra API gratuita deportiva/scraping local):** Para consultar partidos del Málaga CF en La Rosaleda.
  - **OpenAI API / Anthropic API:** Conexión con LLM configurando un System Prompt específico (Acento de Málaga, expresiones, límites de respuesta).
- **Calendario (.ics):** Generación de ficheros `.ics` directamente en frontend usando la librería `ics` de JavaScript o mediante una función helper nativa en JS para evitar dependencias innecesarias.
- **Sistema de Diseño:** Estilo limpio, fresco y mediterráneo con fondo blanco predominante, toques de azul mediterráneo en cabeceras y elementos interactivos, y acentos puntuales de naranja cálido para precios y alertas. Ver detalles en `docs/DESIGN.md`.

## 🚫 5. Fuera de Alcance (Out of Scope)
*Evitar el "scope creep".*

- [ ] Sistema de compras de entradas real (se redirigirá a enlaces externos como Ticketmaster).
- [ ] Autenticación OAuth completa de cuentas de Google/Microsoft (se sustituye por el estándar de exportación universal `.ics` que no requiere credenciales).
- [ ] Autenticación de usuario con base de datos para producción (el estado se mantendrá local en la sesión del navegador / LocalStorage).

## ⚠️ 6. Riesgos y Mitigación
*Anticipar problemas.*

- **Riesgo:** Límites de peticiones (Rate limits) o expiración de claves en las APIs externas (Ticketmaster, OpenAI).
  - **Mitigación:** Almacenamiento en caché de los eventos consultados en el backend durante 1 hora y provisión de un conjunto de eventos mockup locales en caso de caída o desconexión de la API.
- **Riesgo de Seguridad en LLMs (Prompt Injection):** Que los usuarios manipulen el chat para desviar el bot de Málaga a otros temas o realicen inyección de prompts.
  - **Mitigación:** System Prompt robusto con reglas estrictas de retorno ("Si te preguntan algo ajeno a Málaga o eventos, reconduce la conversación amablemente con acento malagueño").
- **Riesgo de Consumo de Contexto por IA:** El chat conversacional de eventos genera muchas llamadas al LLM.
  - **Mitigación:** Mantener un historial de chat corto en la sesión (últimos 10 mensajes) para controlar el tamaño del context window.

## ❓ 7. Preguntas Abiertas
- [ ] ¿Es necesario usar la API real de fútbol o podemos mockear la agenda del Málaga CF al ser una lista de partidos fija y conocida? (Se sugiere mockup para evitar registros de APIs deportivas complejas).
- [ ] ¿Qué proveedor de LLM se utilizará para la personalidad del Boquerón? (Se propone la API de OpenAI GPT-4o-mini o Gemini 1.5 Flash por coste y latencia).

## 🧪 8. Criterios de Evaluación y Evals (No Deterministas)
- [ ] **Conformidad de Formato:** El LLM debe retornar el plan propuesto en una estructura JSON limpia para que el frontend renderice las tarjetas adecuadamente.
- [ ] **Filtro de Localización:** Evaluaremos que al menos el 95% de las recomendaciones correspondan a ubicaciones en la provincia de Málaga.
- [ ] **Rúbrica de Personalidad (Eval):** El asistente debe incluir modismos malagueños en cada respuesta sin perder la coherencia de la recomendación de eventos.