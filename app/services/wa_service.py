"""Service for sending WhatsApp notifications via Meta Graph API."""
import logging
import httpx
from app.core.config import settings

async def send_wa_notification(payload: dict):
    """Send a WhatsApp notification with the given payload."""
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": settings.FONNTE_TOKEN,
        "Content-Type": "application/json"
    }

    message_text = (
        f"*Laporan Baru* (Urgensi: {payload.get('urgensi')})\n"
        f"Dinas: {payload.get('kategori_dinas')}\n"
        f"Lokasi: {payload.get('kecamatan')}\n"
        f"Keluhan: {payload.get('keluhan_teks_bebas')}"
    )

    # Resolve target from mapping based on kategori_dinas
    kategori = payload.get("kategori_dinas", "Tidak Diketahui")
    target = settings.DINAS_TARGET_MAPPING.get(kategori, settings.DINAS_TARGET_MAPPING["Dinas Umum"])

    data = {
        "target": target,
        "message": message_text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            logging.info("WhatsApp notification sent successfully.")
        except Exception as e: # pylint: disable=broad-exception-caught
            logging.error("Failed to send WA notification: %s", e)
