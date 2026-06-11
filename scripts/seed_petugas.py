import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.models import Petugas
from app.services.auth_service import hash_password

# Muat variabel dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def seed_petugas():
    print("Memulai proses seeding petugas...")
    if not DATABASE_URL or "YOUR-PASSWORD" in DATABASE_URL:
        print("ERROR: Kredensial DATABASE_URL tidak valid di .env")
        return

    engine = create_async_engine(
        DATABASE_URL,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0
        }
    )
    
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Periksa apakah petugas 'admin' sudah terdaftar
        stmt = select(Petugas).where(Petugas.username == "admin")
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            print("Petugas 'admin' sudah terdaftar di database. Seeding dilewati.")
            await engine.dispose()
            return

        # Hash password petugas
        pwd_hash = hash_password("admin123")
        admin = Petugas(
            username="admin",
            password_hash=pwd_hash,
            nama_dinas="Dinas Umum"
        )
        session.add(admin)
        await session.commit()
        print("✅ Seeding BERHASIL! Akun petugas 'admin' dengan password 'admin123' telah dibuat.")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_petugas())
