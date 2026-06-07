from pydantic import BaseModel, Field
from typing import Optional

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
