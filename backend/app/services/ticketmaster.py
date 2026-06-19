# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

import datetime
import requests
import time
from typing import List, Dict, Any
from app.config import settings

# Caché en memoria para evitar llamadas excesivas
# Estructura: {"timestamp": float, "data": List[Dict]}
_events_cache: Dict[str, Any] = {"timestamp": 0, "data": []}
CACHE_DURATION = 3600  # 1 hora en segundos

def get_mock_events() -> List[Dict[str, Any]]:
    """Genera una lista de eventos ficticios y realistas en Málaga ajustados dinámicamente al día de hoy."""
    today = datetime.date.today()
    
    # Formateadores de fechas legibles y strings ISO para .ics
    def make_dates(days_delta: int, hour: int = 20) -> Dict[str, str]:
        event_date = today + datetime.timedelta(days=days_delta)
        event_datetime = datetime.datetime.combine(event_date, datetime.time(hour, 0))
        return {
            "date": event_date.strftime("%Y-%m-%d"),
            "formatted_date": event_date.strftime("%d/%m/%Y"),
            "iso_start": event_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "iso_end": (event_datetime + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    d1 = make_dates(1, 21)  # Mañana a las 21:00
    d2 = make_dates(2, 18)  # Pasado mañana a las 18:00
    d3 = make_dates(4, 22)  # En 4 días a las 22:00
    d4 = make_dates(6, 20)  # En 6 días a las 20:00
    d5 = make_dates(9, 19)  # En 9 días a las 19:00
    d6 = make_dates(12, 21) # En 12 días a las 21:00

    return [
        {
            "id": "mock_event_1",
            "title": "Málaga CF vs Real Zaragoza",
            "category": "Deportes",
            "date": d2["date"],
            "time": "18:00",
            "formatted_date": d2["formatted_date"],
            "iso_start": d2["iso_start"],
            "iso_end": d2["iso_end"],
            "price": 15.0,
            "currency": "EUR",
            "location": "Estadio La Rosaleda, Málaga",
            "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=600&q=80",
            "description": "Partido oficial de fútbol en La Rosaleda. ¡Ven a apoyar al equipo boquerón frente al Zaragoza en una tarde de pura pasión malaguista!"
        },
        {
            "id": "mock_event_2",
            "title": "Concierto de Estopa — Gira 2026",
            "category": "Música",
            "date": d3["date"],
            "time": "22:00",
            "formatted_date": d3["formatted_date"],
            "iso_start": d3["iso_start"],
            "iso_end": d3["iso_end"],
            "price": 35.0,
            "currency": "EUR",
            "location": "Auditorio Municipal Cortijo de Torres, Málaga",
            "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80",
            "description": "Los hermanos Muñoz llegan a Málaga para repasar todos sus grandes éxitos de rumba rock en un concierto único al aire libre."
        },
        {
            "id": "mock_event_3",
            "title": "Festival Marenostrum Fuengirola",
            "category": "Festivales",
            "date": d5["date"],
            "time": "19:00",
            "formatted_date": d5["formatted_date"],
            "iso_start": d5["iso_start"],
            "iso_end": d5["iso_end"],
            "price": 45.0,
            "currency": "EUR",
            "location": "Loma del Castillo Sohail, Fuengirola",
            "image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80",
            "description": "Disfruta de uno de los mejores festivales de la Costa del Sol en un entorno medieval único junto al mar. Artistas nacionales e internacionales."
        },
        {
            "id": "mock_event_4",
            "title": "El Barbero de Sevilla — Ópera",
            "category": "Culturales",
            "date": d6["date"],
            "time": "20:00",
            "formatted_date": d6["formatted_date"],
            "iso_start": d6["iso_start"],
            "iso_end": d6["iso_end"],
            "price": 20.0,
            "currency": "EUR",
            "location": "Teatro Cervantes, Málaga",
            "image": "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?auto=format&fit=crop&w=600&q=80",
            "description": "Representación magistral de la famosa ópera buffa de Gioachino Rossini. Una cita cultural imprescindible en el corazón de Málaga."
        },
        {
            "id": "mock_event_5",
            "title": "Málaga Jazz Festival",
            "category": "Música",
            "date": d4["date"],
            "time": "20:00",
            "formatted_date": d4["formatted_date"],
            "iso_start": d4["iso_start"],
            "iso_end": d4["iso_end"],
            "price": 0.0,
            "currency": "EUR",
            "location": "Plaza de la Constitución, Málaga",
            "image": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&w=600&q=80",
            "description": "Conciertos de jazz al aire libre gratuitos con el mejor ambiente en el centro histórico de la ciudad. Entrada libre hasta completar aforo."
        },
        {
            "id": "mock_event_6",
            "title": "Visita Nocturna Guiada a la Alcazaba",
            "category": "Culturales",
            "date": d1["date"],
            "time": "21:00",
            "formatted_date": d1["formatted_date"],
            "iso_start": d1["iso_start"],
            "iso_end": d1["iso_end"],
            "price": 5.0,
            "currency": "EUR",
            "location": "La Alcazaba, Málaga",
            "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=600&q=80",
            "description": "Recorre el palacio fortaleza de época musulmana bajo la luz de las estrellas, descubriendo su historia y sus impresionantes vistas de la bahía."
        }
    ]

def get_events(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """Consulta la API de Ticketmaster para Málaga, usando caché interna y fallback a mockups."""
    global _events_cache
    
    current_time = time.time()
    
    # Retornar caché si está vigente
    if not force_refresh and _events_cache["data"] and (current_time - _events_cache["timestamp"] < CACHE_DURATION):
        return _events_cache["data"]
        
    # Si no hay API Key configurada, servir mockups directamente
    if not settings.is_ticketmaster_configured:
        mock_data = get_mock_events()
        _events_cache = {"timestamp": current_time, "data": mock_data}
        return mock_data
        
    try:
        # Consulta a Ticketmaster API para eventos en Málaga
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "city": "Málaga",
            "size": 20,
            "sort": "date,asc"
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        events = []
        embedded = data.get("_embedded", {})
        ticketmaster_events = embedded.get("events", [])
        
        for e in ticketmaster_events:
            # Mapear categorías de Ticketmaster a nuestras categorías
            segment = e.get("classifications", [{}])[0].get("segment", {}).get("name", "Otros")
            category = "Otros"
            if segment == "Music":
                category = "Música"
            elif segment == "Sports":
                category = "Deportes"
            elif segment == "Arts & Theatre":
                category = "Culturales"
            elif segment == "Film" or segment == "Miscellaneous":
                category = "Culturales"

            # Parsear fecha y hora
            dates = e.get("dates", {})
            start = dates.get("start", {})
            local_date = start.get("localDate", "")
            local_time = start.get("localTime", "20:00")[:5]
            
            # Fechas formateadas
            dt_str = f"{local_date}T{local_time}:00"
            try:
                dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
                formatted_date = dt.strftime("%d/%m/%Y")
                iso_start = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                iso_end = (dt + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                formatted_date = local_date
                iso_start = f"{local_date}T20:00:00Z"
                iso_end = f"{local_date}T22:00:00Z"

            # Parsear precio
            price_info = e.get("priceRanges", [{}])[0]
            price = price_info.get("min", 0.0) if price_info else 0.0
            currency = price_info.get("currency", "EUR") if price_info else "EUR"

            # Obtener mejor imagen
            images = e.get("images", [])
            image_url = images[0].get("url", "") if images else "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80"
            for img in images:
                if img.get("ratio") == "16_9" and 500 <= img.get("width", 0) <= 1000:
                    image_url = img.get("url")
                    break

            # Localización
            venue = e.get("_embedded", {}).get("venues", [{}])[0]
            location = f"{venue.get('name', 'Málaga')}, Málaga"

            events.append({
                "id": e.get("id"),
                "title": e.get("name"),
                "category": category,
                "date": local_date,
                "time": local_time,
                "formatted_date": formatted_date,
                "iso_start": iso_start,
                "iso_end": iso_end,
                "price": float(price),
                "currency": currency,
                "location": location,
                "image": image_url,
                "description": e.get("info", f"Evento de {category} en Málaga. ¡No te lo pierdas!")
            })
            
        if not events:
            # Si la consulta no dio errores pero no hay eventos, usar mockup
            events = get_mock_events()
            
        _events_cache = {"timestamp": current_time, "data": events}
        return events
        
    except Exception as e:
        print(f"Error consultando Ticketmaster API: {e}. Usando mockups como fallback.")
        # Fallback en caso de error
        mock_data = get_mock_events()
        _events_cache = {"timestamp": current_time, "data": mock_data}
        return mock_data
