from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.db.models import Pelapor, LaporanMentah, TriaseAI
from app.schemas import LaporanCreate, Token, UserLogin
from app.tasks import run_triage_and_notify
import jwt
from datetime import datetime, timedelta

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "supersecretkeylapor_kita" 
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=8)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

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
    stmt = select(Pelapor).where(Pelapor.nik == nik)
    res = await db.execute(stmt)
    pelapor = res.scalar_one_or_none()
    
    if not pelapor:
        pelapor = Pelapor(nik=nik, nama=nama, no_hp=no_hp)
        db.add(pelapor)
        await db.flush()

    laporan_baru = LaporanMentah(
        pelapor_id=pelapor.id,
        kecamatan=kecamatan,
        keluhan_teks_bebas=keluhan
    )
    db.add(laporan_baru)
    await db.commit()
    await db.refresh(laporan_baru)

    background_tasks.add_task(run_triage_and_notify, laporan_baru.id, keluhan)

    return {
        "status": "success",
        "message": f"Laporan Anda berhasil diterima! Simpan KODE TIKET Anda untuk pelacakan: {laporan_baru.kode_tiket}",
        "kode_tiket": laporan_baru.kode_tiket
    }

@router.get("/track-ticket/{kode_tiket}")
async def track_ticket(kode_tiket: str, db: AsyncSession = Depends(get_db)):
    stmt = select(LaporanMentah).where(LaporanMentah.kode_tiket == kode_tiket)
    res = await db.execute(stmt)
    laporan = res.scalar_one_or_none()
    
    if not laporan:
        raise HTTPException(status_code=404, detail="Kode tiket tidak ditemukan.")
        
    stmt_triase = select(TriaseAI).where(TriaseAI.laporan_id == laporan.id)
    res_triase = await db.execute(stmt_triase)
    triase = res_triase.scalar_one_or_none()
    
    return {
        "kode_tiket": laporan.kode_tiket,
        "tanggal": laporan.timestamp,
        "kecamatan": laporan.kecamatan,
        "status_ai": triase.status_json if triase else "Sedang dianalisis AI",
        "dinas_tujuan": triase.kategori_dinas if triase else "-",
        "urgensi": triase.urgensi if triase else "-",
        "status_proses": triase.status_proses if triase else "Menunggu"
    }

@router.post("/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin_dinas" and password == "pemerintah123":
        access_token = create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Username atau password salah")

@router.get("/admin/dashboard-stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    total = await db.execute(select(func.count(LaporanMentah.id)))
    accepted = await db.execute(select(func.count(TriaseAI.id)).where(TriaseAI.status_json == "ACCEPTED"))
    rejected = await db.execute(select(func.count(TriaseAI.id)).where(TriaseAI.status_json == "REJECTED"))
    
    return {
        "total_laporan": total.scalar(),
        "accepted_ai": accepted.scalar(),
        "rejected_ai": rejected.scalar()
    }