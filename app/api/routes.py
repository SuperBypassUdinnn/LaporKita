"""API routes for LaporKita application."""
import os
import random
import string
from typing import Optional
from fastapi import APIRouter, Request, BackgroundTasks, Form, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Pelapor, LaporanMentah, TriaseAI
from app.tasks import run_triage_and_notify
from app.services.auth_service import decode_access_token
from app.core.config import settings

router = APIRouter()

# Ensure templates directory exists so it doesn't crash if empty
os.makedirs("app/templates", exist_ok=True)
templates = Jinja2Templates(directory="app/templates")

def generate_ticket_code() -> str:
    """Generate a random 6-character uppercase alphanumeric ticket code."""
    chars = string.ascii_uppercase + string.digits
    return "LK-" + "".join(random.choices(chars, k=6))

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main index page."""
    return templates.TemplateResponse(request=request, name="index.html")

# pylint: disable=too-many-arguments, too-many-positional-arguments
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
    """Handle report submission from the form."""
    # Check if pelapor already exists by NIK
    stmt = select(Pelapor).where(Pelapor.nik == nik)
    result = await db.execute(stmt)
    pelapor = result.scalar_one_or_none()

    if not pelapor:
        pelapor = Pelapor(nik=nik, nama=nama, no_hp=no_hp)
        db.add(pelapor)
        await db.commit()
        await db.refresh(pelapor)
    else:
        # Update nama or no_hp if they changed
        if pelapor.nama != nama or pelapor.no_hp != no_hp:
            pelapor.nama = nama
            pelapor.no_hp = no_hp
            await db.commit()
            await db.refresh(pelapor)

    # Generate unique ticket code
    while True:
        kode_tiket = generate_ticket_code()
        check_stmt = select(LaporanMentah).where(LaporanMentah.kode_tiket == kode_tiket)
        check_res = await db.execute(check_stmt)
        if not check_res.scalar_one_or_none():
            break

    laporan = LaporanMentah(
        pelapor_id=pelapor.id,
        kecamatan=kecamatan,
        keluhan_teks_bebas=keluhan,
        kode_tiket=kode_tiket
    )
    db.add(laporan)
    await db.commit()
    await db.refresh(laporan)

    background_tasks.add_task(run_triage_and_notify, laporan.id, keluhan)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "message": "Laporan sedang diproses AI",
            "kode_tiket": kode_tiket
        }
    )

@router.get("/lacak", response_class=HTMLResponse)
async def lacak_page(request: Request):
    """Render the complaint tracking page."""
    return templates.TemplateResponse(request=request, name="lacak.html")

@router.get("/api/lacak/{kode}")
async def get_lacak_status(kode: str, db: AsyncSession = Depends(get_db)):
    """API endpoint to get the status of a report by its ticket code."""
    stmt = (
        select(LaporanMentah, TriaseAI)
        .outerjoin(TriaseAI, LaporanMentah.id == TriaseAI.laporan_id)
        .where(LaporanMentah.kode_tiket == kode.upper())
    )
    result = await db.execute(stmt)
    row = result.first()

    if not row:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Kode tiket tidak ditemukan."}
        )

    laporan, triase = row

    status_val = "MENUNGGU"
    kategori = "-"
    urgensi = "-"
    if triase:
        status_val = triase.status_json
        kategori = triase.kategori_dinas
        urgensi = triase.urgensi

    return {
        "kode_tiket": laporan.kode_tiket,
        "timestamp": laporan.timestamp.isoformat() if laporan.timestamp else None,
        "status": status_val,
        "kategori_dinas": kategori,
        "urgensi": urgensi,
        "kecamatan": laporan.kecamatan,
        "keluhan": laporan.keluhan_teks_bebas
    }

@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request, error: Optional[str] = None, success: Optional[str] = None):
    """Render the admin login page."""
    return templates.TemplateResponse(request=request, name="login.html", context={"error": error, "success": success})

@router.post("/admin/login")
async def login_post(
    username: str = Form(...),
    password: str = Form(...),
):
    """Handle admin login submission."""
    from app.services.auth_service import create_access_token
    if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
        return RedirectResponse(
            url="/admin/login?error=Username+atau+password+salah", 
            status_code=status.HTTP_303_SEE_OTHER
        )

    token = create_access_token(data={"sub": username})
    response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.get("/admin/logout")
async def logout():
    """Handle admin logout by clearing cookies."""
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render the admin dashboard page."""
    access_token = request.cookies.get("access_token")
    if not access_token:
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    
    payload = decode_access_token(access_token)
    if not payload or "sub" not in payload:
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)

    if payload["sub"] != settings.ADMIN_USERNAME:
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)

    petugas_context = {
        "username": settings.ADMIN_USERNAME,
        "nama_dinas": "Administrator"
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"petugas": petugas_context}
    )

@router.get("/api/admin/statistik")
async def get_dashboard_statistik(request: Request, db: AsyncSession = Depends(get_db)):
    """API endpoint for dashboard statistics."""
    access_token = request.cookies.get("access_token")
    if not access_token or not decode_access_token(access_token):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized"})

    # Count total reports
    total_stmt = select(func.count(LaporanMentah.id))
    total_res = await db.execute(total_stmt)
    total_count = total_res.scalar() or 0

    # Count REJECTED reports
    rejected_stmt = select(func.count(LaporanMentah.id)).join(TriaseAI, LaporanMentah.id == TriaseAI.laporan_id).where(TriaseAI.status_json == "REJECTED")
    rejected_res = await db.execute(rejected_stmt)
    rejected_count = rejected_res.scalar() or 0

    # Count per Dinas (only for ACCEPTED ones)
    dinas_stmt = (
        select(TriaseAI.kategori_dinas, func.count(TriaseAI.id))
        .where(TriaseAI.status_json == "ACCEPTED")
        .group_by(TriaseAI.kategori_dinas)
    )
    dinas_res = await db.execute(dinas_stmt)
    per_dinas = [{"dinas": row[0], "jumlah": row[1]} for row in dinas_res.all()]

    # Count per Urgensi (only for ACCEPTED ones)
    urgensi_stmt = (
        select(TriaseAI.urgensi, func.count(TriaseAI.id))
        .where(TriaseAI.status_json == "ACCEPTED")
        .group_by(TriaseAI.urgensi)
    )
    urgensi_res = await db.execute(urgensi_stmt)
    per_urgensi = [{"urgensi": row[0], "jumlah": row[1]} for row in urgensi_res.all()]

    return {
        "total_laporan": total_count,
        "ditolak_ai": rejected_count,
        "per_dinas": per_dinas,
        "per_urgensi": per_urgensi
    }

@router.get("/api/admin/laporan")
async def get_dashboard_laporan(request: Request, db: AsyncSession = Depends(get_db)):
    """API endpoint for dashboard report list."""
    access_token = request.cookies.get("access_token")
    if not access_token or not decode_access_token(access_token):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized"})

    stmt = (
        select(LaporanMentah, TriaseAI, Pelapor)
        .outerjoin(TriaseAI, LaporanMentah.id == TriaseAI.laporan_id)
        .join(Pelapor, LaporanMentah.pelapor_id == Pelapor.id)
        .order_by(LaporanMentah.timestamp.desc())
    )
    result = await db.execute(stmt)
    rows = result.all()

    reports = []
    for laporan, triase, pelapor in rows:
        status_val = "MENUNGGU"
        kategori = "-"
        urgensi = "-"
        if triase:
            status_val = triase.status_json
            kategori = triase.kategori_dinas
            urgensi = triase.urgensi

        reports.append({
            "kode_tiket": laporan.kode_tiket or "-",
            "kecamatan": laporan.kecamatan,
            "keluhan": laporan.keluhan_teks_bebas,
            "kategori_dinas": kategori,
            "urgensi": urgensi,
            "status": status_val,
            "timestamp": laporan.timestamp.isoformat() if laporan.timestamp else None,
            "nama_pelapor": pelapor.nama,
            "nik_pelapor": pelapor.nik,
            "no_hp_pelapor": pelapor.no_hp
        })

    return reports
