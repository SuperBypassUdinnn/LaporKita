"""Service for interacting with the Google Gemini LLM."""
import json
import logging
import google.generativeai as genai
from app.core.config import settings
from app.core.prompts import TRIASE_SYSTEM_PROMPT
from app.schemas import TriaseResponse

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=TRIASE_SYSTEM_PROMPT)

async def process_triage(text: str) -> TriaseResponse:
    """Process the report text using Gemini to classify and triage."""
    try:
        response = await model.generate_content_async(
            text,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        data = json.loads(response.text)
        return TriaseResponse(**data)
    except Exception as e: # pylint: disable=broad-exception-caught
        logging.error("Error processing triage: %s", e)
        return TriaseResponse(kategori_dinas="Tidak Diketahui", urgensi="Rendah", status="REJECTED")
