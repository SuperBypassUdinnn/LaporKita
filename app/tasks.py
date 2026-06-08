"""Background tasks for processing reports."""
import logging
import uuid
from sqlalchemy import select
from app.services.llm_service import process_triage
from app.services.wa_service import send_wa_notification
from app.db.database import AsyncSessionLocal
from app.db.models import LaporanMentah, TriaseAI

async def run_triage_and_notify(laporan_id: uuid.UUID, teks_keluhan: str):
    """Run the AI triage process and send notifications in the background."""
    logging.info("Starting background triage for laporan_id=%s", laporan_id)

    async with AsyncSessionLocal() as db:
        # 1. Process with LLM
        triase_result = await process_triage(teks_keluhan)

        # 2. Save Triase Result to DB
        triase_entry = TriaseAI(
            laporan_id=laporan_id,
            kategori_dinas=triase_result.kategori_dinas,
            urgensi=triase_result.urgensi,
            status_json=triase_result.status
        )
        db.add(triase_entry)
        await db.commit()

        # 3. Send Notification if ACCEPTED
        if triase_result.status == "ACCEPTED":
            stmt = select(LaporanMentah).where(LaporanMentah.id == laporan_id)
            result = await db.execute(stmt)
            laporan = result.scalar_one_or_none()

            if laporan:
                payload = {
                    "urgensi": triase_result.urgensi,
                    "kategori_dinas": triase_result.kategori_dinas,
                    "kecamatan": laporan.kecamatan,
                    "keluhan_teks_bebas": laporan.keluhan_teks_bebas,
                    "no_hp": "TARGET_PHONE"
                }
                await send_wa_notification(payload)
