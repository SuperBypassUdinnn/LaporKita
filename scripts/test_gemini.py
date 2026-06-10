import asyncio
import os
from google import genai
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def test_gemini():
    print("Mencoba koneksi ke Gemini API...")
    
    if not GEMINI_API_KEY or "your_gemini_api_key_here" in GEMINI_API_KEY or "dummy_key_for_now" in GEMINI_API_KEY:
        print("ERROR: Pastikan Anda telah memasukkan GEMINI_API_KEY yang valid di file .env")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents="Ucapkan kata 'Koneksi Sukses!' dalam bahasa Indonesia."
        )
        print("✅ BERHASIL terhubung ke Gemini API dengan gemini-2.5-flash!")
        print(f"Balasan dari AI: {response.text.strip()}")
    except Exception as e:
        print(f"❌ GAGAL terkoneksi dengan gemini-2.5-flash. Alasan: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
