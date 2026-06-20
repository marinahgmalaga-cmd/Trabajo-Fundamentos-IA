@echo off
:: =============================================================================
:: Proyecto 19junio — Sitio web interactivo
:: Copyright (c) 2026 Marina Heezemans
:: Licensed under the MIT License. See LICENSE for details.
:: Built with dbv-specs-ops · https://github.com/davidbuenov/dbv-specs-ops
:: =============================================================================
:: stop.cmd — Detener todos los servidores

echo Boquerones a la calle - Deteniendo servidores...
taskkill /FI "WindowTitle eq Boqueron-Backend*" /T /F 2>nul
taskkill /FI "WindowTitle eq Boqueron-Frontend*" /T /F 2>nul
echo Hasta luego, boqueron!
