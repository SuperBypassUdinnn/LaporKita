"""Pydantic schemas for data validation."""
from pydantic import BaseModel, Field
from typing import Optional, List

class LaporanCreate(BaseModel):
    nik: str = Field(..., title="NIK Pelapor", min_length=16, max_length=16)
    nama: str = Field(..., title="Nama Pelapor")
    no_hp: str = Field(..., title="Nomor HP Pelapor")
    kecamatan: str = Field(..., title="Kecamatan")
    keluhan: str = Field(..., title="Isi Keluhan")

class TriaseResponse(BaseModel):
    kategori_dinas: str
    urgensi: str
    status: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DashboardStats(BaseModel):
    total_laporan: int
    total_accepted: int
    total_rejected_ai: int
    urgensi_stats: dict
    dinas_stats: dict