import asyncio
import os
from dotenv import load_dotenv
import httpx

# Muat variabel dari file .env
load_dotenv()

FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
# Anda dapat mengganti ini dengan Target ID/Tag Fonnte tujuan Anda
TEST_TARGET = os.getenv("WA_GROUP_UMUM", "grup_dinas_umum")

async def test_fonnte():
    print("Mencoba mengirim pesan WhatsApp menggunakan Fonnte API...")
    
    if not FONNTE_TOKEN or "fonnte_token" in FONNTE_TOKEN.lower():
        print("ERROR: Pastikan Anda telah memasukkan FONNTE_TOKEN yang valid di file .env")
        return

    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": FONNTE_TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "target": TEST_TARGET,
        "message": "Pesan Tes dari Sistem LaporKita via Fonnte 🚀"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 200:
                print("✅ BERHASIL mengirim pesan via Fonnte!")
            else:
                print("❌ GAGAL mengirim pesan.")
        except Exception as e:
            print(f"❌ GAGAL terkoneksi ke Fonnte. Alasan: {e}")

if __name__ == "__main__":
    asyncio.run(test_fonnte())
