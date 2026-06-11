import asyncio
import os
from dotenv import load_dotenv
import httpx

# Muat variabel dari file .env (dengan override=True agar perubahan langsung terbaca)
load_dotenv(override=True)

FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
# Anda dapat mengganti ini dengan Target ID/Tag Fonnte tujuan Anda
TEST_TARGET = os.getenv("WA_GROUP_UMUM", "grup_dinas_umum")

async def test_fonnte():
    masked_token = f"{FONNTE_TOKEN[:4]}...{FONNTE_TOKEN[-4:]}" if FONNTE_TOKEN else "None"
    print(f"Token yang terbaca: {masked_token}")
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
                try:
                    res_data = response.json()
                    if res_data.get("status") is True:
                        print("✅ BERHASIL mengirim pesan via Fonnte!")
                    else:
                        reason = res_data.get("reason", "Alasan tidak diketahui")
                        print(f"❌ GAGAL mengirim pesan. Alasan dari Fonnte: {reason}")
                except Exception as parse_err:
                    print(f"❌ GAGAL memproses response JSON dari Fonnte: {parse_err}")
            else:
                print(f"❌ GAGAL mengirim pesan. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"❌ GAGAL terkoneksi ke Fonnte. Alasan: {e}")

if __name__ == "__main__":
    asyncio.run(test_fonnte())
