import google.generativeai as genai
import json
import logging
from app.core.config import settings
from app.core.prompts import TRIASE_SYSTEM_PROMPT
from app.schemas import TriaseResponse

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=TRIASE_SYSTEM_PROMPT)

async def process_triage(text: str) -> TriaseResponse:
    try:
        response = await model.generate_content_async(
            text,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        data = json.loads(response.text)
        return TriaseResponse(**data)
    except Exception as e:
        logging.error(f"Error processing triage: {e}")
        return TriaseResponse(kategori_dinas="Tidak Diketahui", urgensi="Rendah", status="REJECTED")
