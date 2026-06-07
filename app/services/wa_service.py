import httpx
import logging
from app.core.config import settings

async def send_wa_notification(payload: dict):
    url = f"https://graph.facebook.com/v17.0/{settings.WA_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    message_text = (
        f"*Laporan Baru* (Urgensi: {payload.get('urgensi')})\n"
        f"Dinas: {payload.get('kategori_dinas')}\n"
        f"Lokasi: {payload.get('kecamatan')}\n"
        f"Keluhan: {payload.get('keluhan_teks_bebas')}"
    )

    data = {
        "messaging_product": "whatsapp",
        "to": "TARGET_PHONE_NUMBER", # In a real scenario, this would dynamically route based on dinas
        "type": "text",
        "text": {"body": message_text}
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            logging.info("WhatsApp notification sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send WA notification: {e}")
