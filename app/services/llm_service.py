import os
import json
import google.generativeai as genai
from app.schemas import TriaseResponse
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

FEW_SHOT_PROMPT = """
Anda adalah sistem cerdas Triase Otomatis untuk LaporKita. Tugas Anda adalah menganalisis keluhan masyarakat, menentukan dinas tujuan, tingkat urgensi, dan status validitas laporan.

Pilihan Dinas: ["Dinas PU", "Dinas PDAM", "Dinas Perhubungan", "Dinas Kebersihan", "Dinas Sosial", "Dinas Kesehatan", "Dinas Umum"]
Pilihan Urgensi: ["RENDAH", "SEDANG", "TINGGI"]
Pilihan Status: ["ACCEPTED", "REJECTED"]

---
CONTOH 1 (Valid - Dinas PU):
Input: "Ada lubang besar di tengah jalan raya dekat Alun-alun yang membuat banyak motor jatuh malam ini."
Output JSON: {"kategori_dinas": "Dinas PU", "urgensi": "TINGGI", "status": "ACCEPTED"}

CONTOH 2 (Valid - Dinas Kebersihan):
Input: "Sampah di pasar pagi menumpuk sudah 3 hari tidak diangkut, bau busuk menyengat."
Output JSON: {"kategori_dinas": "Dinas Kebersihan", "urgensi": "SEDANG", "status": "ACCEPTED"}

CONTOH 3 (Ditolak / Junk / Tidak Jelas):
Input: "Halo test test 123 sistemnya bagus ya mas."
Output JSON: {"kategori_dinas": "Dinas Umum", "urgensi": "RENDAH", "status": "REJECTED"}

CONTOH 4 (Penanganan Fallback Tumpang Tindih):
Input: "Jalanan banjir karena saluran air tersumbat sampah komunal dan aspalnya sampai mengelupas hancur, mohon dibantu."
Analisis: Kasus ini melibatkan sampah (Kebersihan) dan aspal rusak/banjir (PU). 
Aturan Fallback: Jika deskripsi tumpang tindih secara masif, arahkan ke infrastruktur utama ("Dinas PU") dengan urgensi tinggi.
Output JSON: {"kategori_dinas": "Dinas PU", "urgensi": "TINGGI", "status": "ACCEPTED"}
---

Lakukan analisis pada teks berikut dan kembalikan hanya dalam format JSON murni seperti contoh di atas:
Teks Keluhan: "{teks_keluhan}"
"""

async def process_triage(teks_keluhan: str) -> TriaseResponse:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            FEW_SHOT_PROMPT.format(teks_keluhan=teks_keluhan),
            generation_config={"response_mime_type": "application/json"}
        )
        
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(cleaned_text)
        
        return TriaseResponse(
            kategori_dinas=data.get("kategori_dinas", "Dinas Umum"),
            urgensi=data.get("urgensi", "RENDAH"),
            status=data.get("status", "REJECTED")
        )
    except Exception:
        return TriaseResponse(
            kategori_dinas="Dinas Umum",
            urgensi="RENDAH",
            status="REJECTED"
        )