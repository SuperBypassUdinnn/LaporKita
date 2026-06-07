from fastapi import APIRouter, Request, BackgroundTasks, Form, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Pelapor, LaporanMentah
from app.tasks import run_triage_and_notify
import os

router = APIRouter()

# Ensure templates directory exists so it doesn't crash if empty
os.makedirs("app/templates", exist_ok=True)
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/submit-laporan")
async def submit_laporan(
    background_tasks: BackgroundTasks,
    nik: str = Form(...),
    nama: str = Form(...),
    no_hp: str = Form(...),
    kecamatan: str = Form(...),
    keluhan: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    pelapor = Pelapor(nik=nik, nama=nama, no_hp=no_hp)
    db.add(pelapor)
    await db.commit()
    await db.refresh(pelapor)

    laporan = LaporanMentah(
        pelapor_id=pelapor.id,
        kecamatan=kecamatan,
        keluhan_teks_bebas=keluhan
    )
    db.add(laporan)
    await db.commit()
    await db.refresh(laporan)

    background_tasks.add_task(run_triage_and_notify, laporan.id, keluhan)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Laporan sedang diproses AI"})
