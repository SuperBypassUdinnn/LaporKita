"""Service for interacting with the Google Gemini LLM."""
import asyncio
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
    max_retries = 3
    retry_delay = 2  # detik

    for attempt in range(max_retries):
        try:
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=text,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    system_instruction=TRIASE_SYSTEM_PROMPT,
                )
            )
            data = json.loads(response.text)
            return TriaseResponse(**data)
        except Exception as e: # pylint: disable=broad-exception-caught
            if attempt == max_retries - 1:
                logging.error("Error processing triage after %d attempts: %s", max_retries, e)
                return TriaseResponse(kategori_dinas="Tidak Diketahui", urgensi="Rendah", status="REJECTED")
            
            logging.warning(
                "Gemini API error (attempt %d/%d): %s. Retrying in %d seconds...",
                attempt + 1, max_retries, e, retry_delay
            )
            await asyncio.sleep(retry_delay)
            retry_delay *= 2

