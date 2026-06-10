import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def test_supabase():
    print("Mencoba koneksi ke database...")
    
    # --- DIAGNOSTIK JARINGAN ---
    print("\n--- DIAGNOSTIK JARINGAN ---")
    import socket
    
    # 1. Cek IPv6 Lokal
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.connect(("2001:4860:4860::8888", 80))
        print(f"✅ IPv6 Terdeteksi Aktif. IP Lokal: {s.getsockname()[0]}")
        s.close()
    except Exception as e:
        print(f"❌ IPv6 Tidak Aktif/Tidak Terjangkau: {e}")

    # 2. Cek Resolusi DNS untuk Pooler Host
    host = "aws-1-ap-southeast-1.pooler.supabase.com"
    if DATABASE_URL:
        # Extract host from DATABASE_URL
        try:
            parts = DATABASE_URL.split("@")
            if len(parts) > 1:
                host_port = parts[1].split("/")[0]
                if ":" in host_port:
                    host = host_port.split(":")[0]
                else:
                    host = host_port
        except Exception:
            pass

    print(f"Mencoba resolusi DNS untuk: {host}")
    try:
        ips = socket.getaddrinfo(host, 6543)
        for ip in ips:
            family = "IPv4" if ip[0] == socket.AF_INET else "IPv6"
            print(f"- Terresolusi ke {family}: {ip[4][0]}")
    except Exception as e:
        print(f"❌ Gagal resolusi DNS: {e}")
    print("---------------------------\n")
    
    if not DATABASE_URL or "YOUR-PASSWORD" in DATABASE_URL:
        print("ERROR: Pastikan Anda telah memasukkan password/URL Supabase yang valid di file .env")
        return
        
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0
        }
    )
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("✅ BERHASIL terkoneksi ke Supabase PostgreSQL!")
            print(f"Versi DB: {version}")
    except Exception as e:
        print(f"❌ GAGAL terkoneksi. Alasan: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_supabase())
