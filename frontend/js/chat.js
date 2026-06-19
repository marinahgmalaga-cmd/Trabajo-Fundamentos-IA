// =============================================================================
// Proyecto 19junio — Sitio web interactivo
// Copyright (c) 2026 Marina Heezemans
// Licensed under the MIT License. See LICENSE for details.
// Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
// =============================================================================

import { addToAgenda, downloadICS, isInAgenda } from './calendar.js';

// Historial de conversación para contexto del LLM
let chatHistory = [];

/**
 * Añade un mensaje de agente (El Boquerón) al DOM del chat.
 * @param {string} text - El texto de la respuesta.
 */
export function appendAgentMessage(text) {
  const container = document.getElementById('chat-messages');
  if (!container) return;

  const el = document.createElement('div');
  el.className = 'message agent';
  el.innerHTML = `
    <div class="agent-avatar">🐟</div>
    <div class="bubble">${text}</div>`;
  container.appendChild(el);
  scrollToBottom();

  chatHistory.push({ role: 'assistant', content: text });
}

/**
 * Añade un mensaje del usuario al DOM del chat.
 * @param {string} text
 */
export function appendUserMessage(text) {
  const container = document.getElementById('chat-messages');
  if (!container) return;

  const el = document.createElement('div');
  el.className = 'message user';
  el.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
  container.appendChild(el);
  scrollToBottom();

  chatHistory.push({ role: 'user', content: text });
}

/**
 * Muestra el indicador de "El Boquerón está escribiendo...".
 * @returns {HTMLElement} El elemento creado, para poder eliminarlo después.
 */
export function showTypingIndicator() {
  const container = document.getElementById('chat-messages');
  if (!container) return null;

  const el = document.createElement('div');
  el.className = 'message agent';
  el.id = 'typing-indicator';
  el.innerHTML = `
    <div class="agent-avatar">🐟</div>
    <div class="bubble">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>`;
  container.appendChild(el);
  scrollToBottom();
  return el;
}

/**
 * Elimina el indicador de escritura del DOM.
 */
export function hideTypingIndicator() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

/**
 * Inserta un grupo de tarjetas de eventos recomendados en el flujo del chat.
 * @param {Array<Object>} events - Array de objetos de eventos a mostrar.
 */
export function appendEventCards(events) {
  const container = document.getElementById('chat-messages');
  if (!container || events.length === 0) return;

  const wrapperEl = document.createElement('div');
  wrapperEl.className = 'chat-events-container';

  events.forEach(event => {
    const inAgenda = isInAgenda(event.id);
    const priceStr  = event.price === 0
      ? '<span class="event-price gratis">¡Gratis!</span>'
      : `<span class="event-price">${event.price} ${event.currency}</span>`;

    const tagClass = event.category.toLowerCase();

    const cardEl = document.createElement('div');
    cardEl.className = 'event-card';
    cardEl.dataset.eventId = event.id;
    cardEl.innerHTML = `
      <img src="${event.image}" alt="${event.title}" class="event-card-img" onerror="this.src='https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80'">
      <div class="event-card-content">
        <div class="event-card-header">
          <h4>${event.title}</h4>
          <span class="event-tag ${tagClass}">${event.category}</span>
        </div>
        <div class="event-details">
          <span>📅 ${event.formatted_date}</span>
          <span>🕐 ${event.time}</span>
          <span>📍 ${event.location}</span>
        </div>
        <div class="event-card-footer">
          ${priceStr}
          <button
            class="action-btn ${inAgenda ? 'added' : ''}"
            data-id="${event.id}"
            ${inAgenda ? 'disabled' : ''}
          >
            ${inAgenda ? '✅ En tu agenda' : '📅 Agendar Plan'}
          </button>
        </div>
      </div>`;

    // Listener del botón "Agendar Plan"
    const btn = cardEl.querySelector('.action-btn');
    if (btn && !inAgenda) {
      btn.addEventListener('click', () => {
        addToAgenda(event);
        downloadICS(event);
        btn.textContent = '✅ En tu agenda';
        btn.classList.add('added');
        btn.disabled = true;
      });
    }

    wrapperEl.appendChild(cardEl);
  });

  container.appendChild(wrapperEl);
  scrollToBottom();
}

/**
 * Limpia el historial de chat y el DOM de mensajes.
 */
export function clearChat() {
  chatHistory = [];
  const container = document.getElementById('chat-messages');
  if (container) container.innerHTML = '';
}

/**
 * Retorna el historial de conversación actual.
 */
export function getChatHistory() {
  return chatHistory;
}

// --- Helpers ---

function scrollToBottom() {
  const container = document.getElementById('chat-messages');
  if (container) {
    requestAnimationFrame(() => {
      container.scrollTop = container.scrollHeight;
    });
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
