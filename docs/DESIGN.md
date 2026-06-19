# 🎨 Sistema de Diseño: Boquerón Plan

> **Fase:** `/spec` (Especificación Visual)
> **Estado:** Validado
> **Última Revisión:** 2026-06-19
> **Aplica a:** Web Boquerón Plan

---

> 📐 Inspirado en el estándar **[design.md](https://github.com/google-labs-code/design.md)** de Google Labs — un formato abierto para describir identidades visuales a agentes de codificación.

---

```yaml
# ────────────────────────────────────────────────
# DESIGN TOKENS — Legibles por la IA y por máquina
# ────────────────────────────────────────────────
version: alpha
name: "Boquerón Plan"
description: "Estilo limpio, fresco y mediterráneo con fondo blanco predominante, toques de azul mediterráneo en cabeceras y elementos interactivos, y acentos puntuales de naranja cálido para precios y alertas."

# COLORES
# Usa códigos HEX. El campo "on-X" es el color de texto que va sobre el color "X".
colors:
  primary:      "#2B6CB0"   # Azul Mediterráneo (para headers, botones de acción y burbujas de la IA)
  secondary:    "#ED8936"   # Naranja suave (acento cálido para precios, alertas y tags destacados)
  accent:       "#2B6CB0"   # Azul para botones primarios / CTAs
  neutral:      "#FFFFFF"   # Blanco predominante (fondo general de la web)
  surface:      "#FFFFFF"   # Blanco para tarjetas, secciones y chat
  on-primary:   "#FFFFFF"   # Texto blanco sobre fondo azul
  on-surface:   "#2D3748"   # Gris oscuro / azul marino para textos principales (evitando negro puro)
  on-neutral:   "#718096"   # Gris medio para textos secundarios / fechas / ubicaciones
  error:        "#E53E3E"   # Rojo para errores
  success:      "#38A169"   # Verde para éxito
  warning:      "#ED8936"   # Naranja/amarillo suave para advertencias y precios

# SIN MODO OSCURO (Desactivado explícitamente según requerimientos de estilo fresco y diurno)
dark: null

# TIPOGRAFÍA
typography:
  heading:
    fontFamily: "Outfit"
    fontSize:   2.25rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  subheading:
    fontFamily: "Outfit"
    fontSize:   1.35rem
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Inter"
    fontSize:   1rem
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter"
    fontSize:   0.875rem
    fontWeight: 600
    letterSpacing: "0.02em"
  caption:
    fontFamily: "Inter"
    fontSize:   0.75rem
    fontWeight: 400

# BORDES Y RADIOS (Líneas limpias y redondeado suave)
rounded:
  none: 0px
  sm:   4px
  md:   8px
  lg:   16px
  xl:   24px
  full: 9999px

# ESPACIADO (escala base 4px)
spacing:
  xs:  4px
  sm:  8px
  md:  16px
  lg:  24px
  xl:  48px
  xxl: 96px

# COMPONENTES — Mapeo de tokens a elementos de UI concretos
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor:       "{colors.on-primary}"
    typography:      "{typography.label}"
    rounded:         "{rounded.full}"
    padding:         "12px 28px"
    transition:      "all 0.2s ease-in-out"
  button-primary-hover:
    backgroundColor: "#1D4F8A"
    transform:       "translateY(-1px)"
  button-secondary:
    backgroundColor: "transparent"
    textColor:       "{colors.primary}"
    rounded:         "{rounded.full}"
    padding:         "12px 28px"
    border:          "2px solid {colors.primary}"
  card:
    backgroundColor: "{colors.surface}"
    rounded:         "{rounded.md}"
    padding:         "{spacing.lg}"
    border:          "1px solid #E2E8F0" # Borde sutil para separar sobre fondo blanco
    box-shadow:      "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)"
  chat-bubble-agent:
    backgroundColor: "#EBF8FF" # Azul muy claro mediterráneo
    textColor:       "{colors.on-surface}"
    rounded:         "18px 18px 18px 2px"
    padding:         "12px 18px"
    border:          "1px solid #BEE3F8"
  chat-bubble-user:
    backgroundColor: "#EDF2F7" # Gris claro suave
    textColor:       "{colors.on-surface}"
    rounded:         "18px 18px 2px 18px"
    padding:         "12px 18px"
  input-chat:
    backgroundColor: "{colors.surface}"
    textColor:       "{colors.on-surface}"
    rounded:         "{rounded.full}"
    padding:         "14px 24px"
    border:          "1.5px solid #E2E8F0"
```

---

## Visión General

La interfaz de **Boquerón Plan** ofrece una experiencia extremadamente limpia, luminosa y fresca. El blanco es el protagonista absoluto de los fondos y contenedores, logrando una sensación de claridad y orden. Los acentos en azul mediterráneo (`#2B6CB0`) estructuran la jerarquía (headers, burbujas de diálogo del agente y botones de acción), mientras que un naranja cálido y suave (`#ED8936`) destaca detalles puntuales como precios o alertas para evitar que el sitio adquiera un carácter frío o corporativo.

---

## 🎨 Colores

- **Fondo General y Tarjetas (`#FFFFFF`):** Dominio absoluto del blanco. Las secciones y tarjetas se separan mediante bordes ultrafinos de color gris suave (`#E2E8F0`) y sombras de mínima intensidad.
- **Azul Mediterráneo (`#2B6CB0`):** Utilizado en la cabecera superior de la aplicación, las burbujas de chat del agente ("El Boquerón"), los botones primarios (como el CTA de "Agendar Plan") y los títulos destacados.
- **Naranja/Amarillo Suave (`#ED8936`):** Tono de acento puntual. Se utiliza de forma dosificada para resaltar precios, tags de eventos patrocinados/destacados o alertas importantes.
- **Texto Principal (`#2D3748`):** Gris oscuro azulado para mantener la coherencia cromática y evitar el contraste plano y fatigante del negro puro.
- **Texto Secundario (`#718096`):** Gris medio para fechas, descripciones secundarias y textos complementarios.

---

## ✍️ Tipografía

- **Fuente de Encabezados (Headings):** `Outfit` — Aporta modernidad y dinamismo a través de sus formas amigables y contemporáneas.
- **Fuente de Cuerpo (Body):** `Inter` — Garantiza la máxima legibilidad en los mensajes de chat y el contenido de las tarjetas.

---

## 🧩 Componentes Clave

### Chat Conversacional
- **Mensajes del Asistente:** Fondo azul claro (`#EBF8FF`), borde sutil (`#BEE3F8`), con el avatar del personaje a la izquierda.
- **Mensajes del Usuario:** Fondo gris claro neutro (`#EDF2F7`) con texto oscuro, alineado a la derecha.
- **Campo de Entrada:** Bordes muy redondeados (`rounded.full`) y sombreado mínimo sobre fondo blanco.

### Tarjetas de Eventos
- Fondo blanco puro, borde gris sutil y sombra suave.
- Las imágenes de los eventos tienen un radio de esquina de `8px`.
- Las etiquetas de precio utilizan el color de acento naranja (`#ED8936`) en un tamaño destacado.
- El botón de acción ("Agendar Plan") utiliza el color azul mediterráneo (`#2B6CB0`).

---

## ✨ Movimiento e Interacción

- **Transiciones:** Micro-interacciones rápidas y precisas (hover en botones a `150ms`).
- **Scroll del Chat:** Los nuevos mensajes se añaden al final del contenedor deslizándose de forma suave para mantener el hilo natural de la lectura.
