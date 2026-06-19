# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

from fastapi import APIRouter, Header, Response, Body
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.services.llm import chat_with_boqueron

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

@router.post("/api/chat")
def post_chat(
    payload: ChatRequest,
    accept: Optional[str] = Header(None)
):
    """Envía un mensaje al asistente 'El Boquerón' y recibe recomendaciones de eventos."""
    result = chat_with_boqueron(
        user_message=payload.message,
        chat_history=payload.history or []
    )
    
    # Negociación de contenido para agentes de IA (Accept: text/markdown)
    if accept and "text/markdown" in accept:
        md = f"### 💬 Mensaje de El Boquerón\n\n{result['message']}\n\n"
        if result['recommended_event_ids']:
            md += f"**Eventos recomendados en esta respuesta (IDs):** {', '.join(result['recommended_event_ids'])}\n"
        return Response(content=md, media_type="text/markdown")
        
    return result
