// =============================================================================
// Proyecto 19junio — Sitio web interactivo
// Copyright (c) 2026 Marina Heezemans
// Licensed under the MIT License. See LICENSE for details.
// Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
// =============================================================================

import { fetchEvents, sendChatMessage } from './api.js';
import {
  appendAgentMessage,
  appendUserMessage,
  showTypingIndicator,
  hideTypingIndicator,
  appendEventCards,
  clearChat,
  getChatHistory
} from './chat.js';
import { renderMiniCalendar, renderAgenda } from './calendar.js';

// --- Application State ---
let allEvents = [];
let activeCategory = 'todos';
let activeMaxPrice = 'all';
let activeDateFilter = 'all';

// --- Initialization ---

async function init() {
  renderMiniCalendar();
  renderAgenda();
  setupEventListeners();

  // Load events from backend
  try {
    allEvents = await fetchEvents();
  } catch (err) {
    console.error('No se pudo conectar con el backend:', err);
    allEvents = [];
  }

  // Initial welcome message from El Boquerón
  appendAgentMessage('¡Alohe, boquerón! 🐟 Soy El Boquerón, tu guía de planes en Málaga.<br><br>Dime qué te apetece: ¿fútbol, conciertos, festivales, cultura...? ¿Qué presupuesto tienes y para cuándo? ¡Y te busco el plan perita sin moverte del sitio!');
}

// --- Event Listeners ---

function setupEventListeners() {
  // Chat form submit
  const form = document.getElementById('chat-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const message = input.value.trim();
      if (!message) return;

      input.value = '';
      input.disabled = true;
      document.querySelector('.send-btn').disabled = true;

      appendUserMessage(message);
      const typingEl = showTypingIndicator();

      try {
        const history = getChatHistory().slice(0, -1); // Excluir el mensaje recién añadido
        const result = await sendChatMessage(message, history);

        hideTypingIndicator();
        appendAgentMessage(result.message);

        // Mostrar eventos recomendados si los hay
        if (result.recommended_event_ids && result.recommended_event_ids.length > 0) {
          const recommendedEvents = allEvents.filter(e =>
            result.recommended_event_ids.includes(e.id)
          );
          if (recommendedEvents.length > 0) {
            appendEventCards(recommendedEvents);
          }
        }

      } catch (err) {
        hideTypingIndicator();
        appendAgentMessage('¡Ay, boquerón, se me ha ido la pinza! 😅 Parece que no puedo conectar con el servidor ahora mismo. ¿Le das un momento y lo intentamos otra vez?');
        console.error('Error en el chat:', err);
      } finally {
        input.disabled = false;
        document.querySelector('.send-btn').disabled = false;
        input.focus();
      }
    });
  }

  // Clear chat button
  const clearBtn = document.getElementById('clear-chat-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      clearChat();
      appendAgentMessage('¡Empezamos de cero, boquerón! ¿Qué plan buscamos hoy por Málaga? 🎉');
    });
  }

  // Category chips
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.dataset.category;
      applyFiltersAndShowEvents();
    });
  });

  // Price filter
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      activeMaxPrice = priceFilter.value;
      applyFiltersAndShowEvents();
    });
  }

  // Date filter
  const dateFilter = document.getElementById('date-filter');
  if (dateFilter) {
    dateFilter.addEventListener('change', () => {
      activeDateFilter = dateFilter.value;
      applyFiltersAndShowEvents();
    });
  }
}

// --- Filter Logic ---

/**
 * Aplica los filtros activos sobre allEvents y muestra una respuesta en el chat.
 */
function applyFiltersAndShowEvents() {
  if (allEvents.length === 0) return;

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const filtered = allEvents.filter(event => {
    // Filtro categoría
    if (activeCategory !== 'todos') {
      if (event.category.toLowerCase() !== activeCategory) return false;
    }

    // Filtro precio
    if (activeMaxPrice !== 'all') {
      const maxPrice = parseFloat(activeMaxPrice);
      if (event.price > maxPrice) return false;
    }

    // Filtro fecha
    if (activeDateFilter !== 'all') {
      const eventDate = new Date(event.date + 'T00:00:00');
      if (activeDateFilter === 'today') {
        const todayStr = today.toISOString().split('T')[0];
        if (event.date !== todayStr) return false;
      } else if (activeDateFilter === 'tomorrow') {
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomorrowStr = tomorrow.toISOString().split('T')[0];
        if (event.date !== tomorrowStr) return false;
      } else if (activeDateFilter === 'weekend') {
        const dayOfWeek = eventDate.getDay(); // 0=Dom, 6=Sab
        if (dayOfWeek !== 0 && dayOfWeek !== 6) return false;
        if (eventDate < today) return false;
      }
    }

    return true;
  });

  // Construir respuesta contextualizada con acento malagueño
  let agentMessage = '';
  const catLabel = activeCategory === 'todos' ? 'planes' : activeCategory;

  if (filtered.length === 0) {
    agentMessage = `¡Cusha, boquerón! No encuentro ${catLabel} con esos filtros para el período seleccionado. Prueba a ampliar las fechas o el presupuesto, ¡que en Málaga siempre hay algo!`;
  } else {
    const priceNote = activeMaxPrice === '0' ? ' ¡Y gratis, perita!' : '';
    agentMessage = `¡Toma ya! 🎉 Aquí te muestro ${filtered.length} ${catLabel} en Málaga con tus filtros.${priceNote}`;
  }

  appendAgentMessage(agentMessage);
  if (filtered.length > 0) {
    appendEventCards(filtered.slice(0, 4)); // Máximo 4 tarjetas por filtrado manual
  }
}

// --- Start ---
document.addEventListener('DOMContentLoaded', init);
