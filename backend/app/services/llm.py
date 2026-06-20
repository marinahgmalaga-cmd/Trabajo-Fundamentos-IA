# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

import json
from typing import List, Dict, Any
from app.config import settings
from app.services.ticketmaster import get_events

SYSTEM_PROMPT = """
Eres 'El Boquerón', un guía local de Málaga amigable, cercano y saleroso.
Tienes un acento malagueño muy marcado y usas de forma natural expresiones locales de Málaga, como:
- 'boquerón' / 'boquerona' (para referirte al usuario)
- 'pechá' (pechá de calor, pechá de gente, pechá de chulo - significa mucho/un montón)
- 'perita' / 'guay' (para decir que algo es genial o muy bueno)
- 'cusha' (para llamar la atención, significa escucha)
- 'alohe' / 'alohe qué pasa' (saludo)
- 'tieso' (sin dinero)
- 'majarón' (loco de gracia)

Tu objetivo es recomendar planes y eventos de Málaga que se te proporcionan en la lista.
Sé alegre, simpático y conciso (máximo 3-4 frases por respuesta). Mantén siempre la conversación en torno a eventos en Málaga. Si te preguntan sobre otra cosa, responde de manera divertida con acento malagueño redirigiendo el tema a los planes de Málaga.

DEBES responder estrictamente en formato JSON con la siguiente estructura:
{
  "message": "Tu respuesta conversacional con acento malagueño",
  "recommended_event_ids": ["id_de_evento_1", "id_de_evento_2"]
}
Solo incluye en `recommended_event_ids` los IDs de los eventos que consideras que mejor coinciden con la petición del usuario, seleccionados de la lista de eventos disponibles que se te proporciona. Si ninguno coincide o la petición es muy general, puedes recomendar 2 o 3 al azar o dejar el array vacío.
"""

def generate_local_response(user_message: str, events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generador local basado en reglas de respuestas con acento malagueño para cuando no hay API Key."""
    msg = user_message.lower()
    
    # Filtrar eventos
    recommended_ids = []
    
    if "futbol" in msg or "partido" in msg or "deporte" in msg or "málaga cf" in msg or "rosaleda" in msg:
        message = "¡Ese Málaga CF en La Rosaleda, boquerón! 💙 Te recomiendo ir a ver el partidazo contra el Zaragoza. ¡Un ambientazo perita asegurado para animar a nuestro equipo!"
        # Buscar el partido en el listado
        football_event = next((e for e in events if e["category"] == "Deportes"), None)
        if football_event:
            recommended_ids.append(football_event["id"])
            
    elif "gratis" in msg or "barato" in msg or "tieso" in msg or "dinero" in msg or "0" in msg:
        message = "¡Cusha, que te veo tieso de dinero! No pasa nada, que en Málaga hay planes de categoría gratis. Vete a la Plaza de la Constitución a escuchar jazz perita por cero euros, ¡música para tus oídos y tu bolsillo!"
        jazz_event = next((e for e in events if e["price"] == 0.0), None)
        if jazz_event:
            recommended_ids.append(jazz_event["id"])
            
    elif "musica" in msg or "concierto" in msg or "cantar" in msg or "estopa" in msg or "festival" in msg:
        message = "¡Pechá de ganas de música que tienes! Estopa va a dar un concierto que va a estar de locos en el Auditorio. O si quieres festival, el Marenostrum en Fuengirola es de lo mejorcito del verano."
        music_events = [e for e in events if e["category"] in ["Música", "Festivales"]]
        recommended_ids = [e["id"] for e in music_events[:2]]
        
    elif "cultura" in msg or "teatro" in msg or "visita" in msg or "historia" in msg or "alcazaba" in msg:
        message = "Málaga tiene pechá de arte y duende, boquerón. Vete a ver la ópera al Teatro Cervantes o haz la visita nocturna a la Alcazaba, que con la fresca de la noche y las luces es de película."
        cultural_events = [e for e in events if e["category"] == "Culturales"]
        recommended_ids = [e["id"] for e in cultural_events[:2]]
        
    else:
        message = "¡Alohe qué pasa, boquerón! ¿Qué te apetece hacer por Málaga? Te puedo buscar conciertos, fútbol en La Rosaleda o algún plan cultural de categoría. Dime tu presupuesto y lo apañamos en un santiamén."
        # Recomendar dos aleatorios de inicio
        recommended_ids = [events[i]["id"] for i in range(min(2, len(events)))]
        
    return {
        "message": message,
        "recommended_event_ids": recommended_ids
    }

def chat_with_boqueron(user_message: str, chat_history: List[Dict[str, str]] = []) -> Dict[str, Any]:
    """Envía la consulta del usuario a Gemini con el contexto de eventos y la personalidad de 'El Boquerón'."""
    events = get_events()
    
    # Si la clave no está configurada, usar el generador local
    if not settings.is_llm_configured:
        return generate_local_response(user_message, events)
        
    try:
        from google import genai
        
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Formatear el listado de eventos para enviarlo al modelo
        events_str = ""
        for e in events:
            events_str += f"- ID: {e['id']} | Título: {e['title']} | Categoría: {e['category']} | Fecha: {e['date']} | Hora: {e['time']} | Precio: {e['price']}{e['currency']} | Lugar: {e['location']}\n"
        
        # Construir el prompt completo con historial de conversación
        full_prompt = SYSTEM_PROMPT + "\n\n"
        full_prompt += f"LISTA DE EVENTOS REALES DISPONIBLES EN MÁLAGA:\n{events_str}\n\n"
        
        # Agregar historial (últimos 8 mensajes para no saturar tokens)
        if chat_history:
            full_prompt += "HISTORIAL DE CONVERSACIÓN RECIENTE:\n"
            for h in chat_history[-8:]:
                role_label = "Usuario" if h["role"] == "user" else "El Boquerón"
                full_prompt += f"{role_label}: {h['content']}\n"
            full_prompt += "\n"
        
        full_prompt += f"MENSAJE ACTUAL DEL USUARIO: {user_message}\n\n"
        full_prompt += "Responde SOLO con el JSON válido, sin texto adicional ni bloques de código."
        
        # Llamar a Gemini con respuesta JSON
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.7,
            }
        )
        
        content = response.text
        result = json.loads(content)
        return {
            "message": result.get("message", "¡Buenas, boquerón!"),
            "recommended_event_ids": result.get("recommended_event_ids", [])
        }
        
    except Exception as e:
        print(f"Error llamando a la API de Gemini: {e}. Usando generador local.")
        return generate_local_response(user_message, events)
