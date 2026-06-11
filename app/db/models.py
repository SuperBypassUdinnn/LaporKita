"""SQLAlchemy database models."""
import uuid
import random
import string
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Uuid
from sqlalchemy.sql import func
from app.db.database import Base

def generate_short_ticket():
    chars = string.ascii_uppercase + string.digits
    return "LK-" + "".join(random.choices(chars, k=6))

class Pelapor(Base):
    __tablename__ = "pelapor"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = Column(String, unique=True, index=True)
    nama = Column(String)
    no_hp = Column(String)

class LaporanMentah(Base):
    __tablename__ = "laporan_mentah"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pelapor_id = Column(Uuid(as_uuid=True), ForeignKey("pelapor.id"))
    kecamatan = Column(String)
    keluhan_teks_bebas = Column(Text)
    kode_tiket = Column(String, unique=True, index=True, default=generate_short_ticket)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class TriaseAI(Base):
    __tablename__ = "triase_ai"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    laporan_id = Column(Uuid(as_uuid=True), ForeignKey("laporan_mentah.id"))
    kategori_dinas = Column(String)
    urgensi = Column(String)
    status_json = Column(String)
    status_proses = Column(String, default="Menunggu Verifikasi")
    waktu_disposisi = Column(DateTime(timezone=True), onupdate=func.now())