// =============================================================================
// Proyecto 19junio — Sitio web interactivo
// Copyright (c) 2026 Marina Heezemans
// Licensed under the MIT License. See LICENSE for details.
// Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
// =============================================================================

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Obtiene la lista de eventos disponibles en Málaga desde el backend.
 * @returns {Promise<Array>}
 */
export async function fetchEvents() {
  const response = await fetch(`${API_BASE_URL}/api/events`);
  if (!response.ok) throw new Error(`Error al cargar eventos: ${response.status}`);
  return response.json();
}

/**
 * Envía un mensaje al asistente El Boquerón y recibe la respuesta con event IDs recomendados.
 * @param {string} message - El mensaje del usuario.
 * @param {Array<{role: string, content: string}>} history - Historial de conversación.
 * @returns {Promise<{message: string, recommended_event_ids: string[]}>}
 */
export async function sendChatMessage(message, history = []) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history })
  });
  if (!response.ok) throw new Error(`Error en el chat: ${response.status}`);
  return response.json();
}
