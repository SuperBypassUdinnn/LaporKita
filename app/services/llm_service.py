"""Service for interacting with the Google Gemini LLM."""
import json
import logging
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.prompts import TRIASE_SYSTEM_PROMPT
from app.schemas import TriaseResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def process_triage(text: str) -> TriaseResponse:
    """Process the report text using Gemini to classify and triage."""
    try:
        response = await client.aio.models.generate_content(
            model='gemini-1.5-flash',
            contents=text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction=TRIASE_SYSTEM_PROMPT,
            )
        )
        data = json.loads(response.text)
        return TriaseResponse(**data)
    except Exception as e: # pylint: disable=broad-exception-caught
        logging.error("Error processing triage: %s", e)
        return TriaseResponse(kategori_dinas="Tidak Diketahui", urgensi="Rendah", status="REJECTED")
