# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, events
from app.config import settings

app = FastAPI(
    title="Boquerón Plan API",
    description="API del asistente conversacional de eventos de Málaga",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde cualquier origen (local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de chat y eventos
app.include_router(chat.router)
app.include_router(events.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "name": "Boquerón Plan API",
        "description": "Busca y agenda eventos en Málaga chateando con el guía local Boquerón",
        "llm_configured": settings.is_llm_configured,
        "ticketmaster_configured": settings.is_ticketmaster_configured
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
