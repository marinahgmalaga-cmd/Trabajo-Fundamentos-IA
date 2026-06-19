# =============================================================================
# Proyecto 19junio — Sitio web interactivo
# Copyright (c) 2026 Marina Heezemans
# Licensed under the MIT License. See LICENSE for details.
# Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
# =============================================================================

import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env si existe
load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TICKETMASTER_API_KEY: str = os.getenv("TICKETMASTER_API_KEY", "")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")

    @property
    def is_llm_configured(self) -> bool:
        return bool(self.OPENAI_API_KEY)

    @property
    def is_ticketmaster_configured(self) -> bool:
        return bool(self.TICKETMASTER_API_KEY)

settings = Settings()
