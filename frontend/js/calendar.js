// =============================================================================
// Proyecto 19junio — Sitio web interactivo
// Copyright (c) 2026 Marina Heezemans
// Licensed under the MIT License. See LICENSE for details.
// Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
// =============================================================================

// Agenda data stored in session (in-memory + LocalStorage)
let scheduledEvents = JSON.parse(localStorage.getItem('boqueron_agenda') || '[]');

// --- ICS Generation ---

/**
 * Genera y descarga un archivo .ics estándar para el evento dado.
 * Usa fechas en formato UTC (Z) para evitar conflictos de zona horaria.
 * @param {Object} event - Objeto de evento con iso_start, iso_end, title, description, location.
 */
export function downloadICS(event) {
  const uid = `${event.id}-${Date.now()}@boqueron-plan.malaga`;
  const dtStamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

  // Formatear fechas al estilo iCalendar (ej: 20260621T200000Z)
  const formatICSDate = (isoStr) => isoStr.replace(/[-:]/g, '').replace('.000', '');

  const dtStart = formatICSDate(event.iso_start);
  const dtEnd   = formatICSDate(event.iso_end);

  const priceStr = event.price === 0 ? 'Entrada gratuita' : `Precio desde ${event.price} ${event.currency}`;

  const icsContent = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Boquerón Plan//Málaga Events//ES',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    `UID:${uid}`,
    `DTSTAMP:${dtStamp}`,
    `DTSTART:${dtStart}`,
    `DTEND:${dtEnd}`,
    `SUMMARY:${event.title}`,
    `DESCRIPTION:${event.description}\\n\\n${priceStr}\\n\\nPlan agendado con Boquerón Plan — Tu guía local de Málaga.`,
    `LOCATION:${event.location}`,
    'STATUS:CONFIRMED',
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n');

  // Descargar el fichero en el navegador
  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `${event.title.replace(/[^a-z0-9]/gi, '_')}.ics`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// --- Agenda Management ---

/**
 * Añade un evento a la agenda interna de la sesión.
 * @param {Object} event
 */
export function addToAgenda(event) {
  if (isInAgenda(event.id)) return;
  scheduledEvents.push(event);
  persistAgenda();
  renderAgenda();
  renderMiniCalendar();
}

/**
 * Elimina un evento de la agenda por su ID.
 * @param {string} eventId
 */
export function removeFromAgenda(eventId) {
  scheduledEvents = scheduledEvents.filter(e => e.id !== eventId);
  persistAgenda();
  renderAgenda();
  renderMiniCalendar();
}

/**
 * Retorna true si el evento ya está en la agenda.
 * @param {string} eventId
 */
export function isInAgenda(eventId) {
  return scheduledEvents.some(e => e.id === eventId);
}

/**
 * Retorna el conjunto de fechas ISO (YYYY-MM-DD) de los eventos agendados.
 */
export function getScheduledDates() {
  return new Set(scheduledEvents.map(e => e.date));
}

function persistAgenda() {
  localStorage.setItem('boqueron_agenda', JSON.stringify(scheduledEvents));
}

// --- Agenda List Renderer ---

export function renderAgenda() {
  const container = document.getElementById('agenda-list');
  const countEl   = document.getElementById('agenda-count');
  if (!container) return;

  countEl.textContent = `${scheduledEvents.length} plan${scheduledEvents.length !== 1 ? 'es' : ''}`;

  if (scheduledEvents.length === 0) {
    container.innerHTML = `
      <div class="empty-agenda">
        <span class="empty-icon">📅</span>
        <p>Aún no has agendado ningún plan. ¡Dile a El Boquerón lo que te apetece o haz clic en "Agendar Plan" en las tarjetas de eventos!</p>
      </div>`;
    return;
  }

  // Ordenar por fecha
  const sorted = [...scheduledEvents].sort((a, b) => a.date.localeCompare(b.date));

  container.innerHTML = sorted.map(e => {
    const priceStr = e.price === 0 ? '🎁 Gratis' : `${e.price} ${e.currency}`;
    return `
      <div class="agenda-item" data-id="${e.id}">
        <div class="agenda-item-info">
          <div class="agenda-item-title">${e.title}</div>
          <div class="agenda-item-meta">📅 ${e.formatted_date} · 🕐 ${e.time} · ${priceStr}</div>
        </div>
        <div class="agenda-actions">
          <button class="agenda-btn" title="Descargar .ics" onclick="window._calendarExport('${e.id}')">
            <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
          </button>
          <button class="agenda-btn delete" title="Eliminar de agenda" onclick="window._calendarRemove('${e.id}')">
            <svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
          </button>
        </div>
      </div>`;
  }).join('');

  // Exponer funciones de callback al contexto global para los eventos onclick inline
  window._calendarExport = (id) => {
    const ev = scheduledEvents.find(e => e.id === id);
    if (ev) downloadICS(ev);
  };
  window._calendarRemove = (id) => {
    removeFromAgenda(id);
    // Actualizar el botón de la tarjeta de evento si está visible
    const cardBtn = document.querySelector(`[data-event-id="${id}"] .action-btn`);
    if (cardBtn) {
      cardBtn.textContent = '📅 Agendar Plan';
      cardBtn.classList.remove('added');
    }
  };
}

// --- Mini Calendar Renderer ---

export function renderMiniCalendar() {
  const container = document.getElementById('mini-calendar');
  if (!container) return;

  const scheduledDates = getScheduledDates();
  const today = new Date();
  const year  = today.getFullYear();
  const month = today.getMonth(); // 0-indexed

  // Cabeceras de día
  const dayHeaders = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    .map(d => `<div class="calendar-day-header">${d}</div>`)
    .join('');

  // Primer día del mes y total de días
  const firstDay = new Date(year, month, 1).getDay(); // 0 = Domingo
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // Ajustar para semanas que empiezan en Lunes
  const startOffset = (firstDay === 0) ? 6 : firstDay - 1;

  let cells = '';

  // Celdas vacías del mes anterior
  for (let i = 0; i < startOffset; i++) {
    cells += `<div class="calendar-day other-month"></div>`;
  }

  // Días del mes actual
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const isToday = (d === today.getDate());
    const hasEvent = scheduledDates.has(dateStr);

    let classes = 'calendar-day';
    if (isToday)   classes += ' today';
    if (hasEvent)  classes += ' has-event';

    const dot = hasEvent ? '<span class="calendar-day-dot"></span>' : '';
    cells += `<div class="${classes}">${d}${dot}</div>`;
  }

  container.innerHTML = dayHeaders + cells;
}
