"""Pydantic schemas for data validation."""
from pydantic import BaseModel, Field

class LaporanCreate(BaseModel):
    """Schema for creating a new report."""
    nik: str = Field(..., title="NIK Pelapor", min_length=16, max_length=16)
    nama: str = Field(..., title="Nama Pelapor")
    no_hp: str = Field(..., title="Nomor HP Pelapor")
    kecamatan: str = Field(..., title="Kecamatan")
    keluhan: str = Field(..., title="Isi Keluhan")

class TriaseResponse(BaseModel):
    """Schema for the AI triage response."""
    kategori_dinas: str
    urgensi: str
    status: str
