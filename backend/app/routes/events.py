# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

from fastapi import APIRouter, Header, Response
from typing import Optional
from app.services.ticketmaster import get_events

router = APIRouter()

@router.get("/api/events")
def read_events(
    force_refresh: bool = False,
    accept: Optional[str] = Header(None)
):
    """Retorna la lista de eventos en Málaga. Soporta negociación de contenido en Markdown."""
    events = get_events(force_refresh=force_refresh)
    
    # Negociación de contenido para agentes de IA (Accept: text/markdown)
    if accept and "text/markdown" in accept:
        markdown_content = "# 📅 Eventos y Planes en Málaga\n\n"
        markdown_content += "Lista de eventos recomendados en Málaga para esta semana:\n\n"
        
        for e in events:
            price_str = "Gratis" if e["price"] == 0.0 else f"{e['price']} {e['currency']}"
            markdown_content += f"### 🎭 {e['title']}\n"
            markdown_content += f"- **Categoría:** {e['category']}\n"
            markdown_content += f"- **Fecha y Hora:** {e['formatted_date']} a las {e['time']}\n"
            markdown_content += f"- **Precio:** {price_str}\n"
            markdown_content += f"- **Ubicación:** {e['location']}\n"
            markdown_content += f"- **Descripción:** {e['description']}\n\n"
            
        return Response(content=markdown_content, media_type="text/markdown")
        
    return events
