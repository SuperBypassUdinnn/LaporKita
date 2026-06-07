from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Pelapor(Base):
    __tablename__ = "pelapor"
    id = Column(Integer, primary_key=True, index=True)
    nik = Column(String, unique=True, index=True)
    nama = Column(String)
    no_hp = Column(String)

class LaporanMentah(Base):
    __tablename__ = "laporan_mentah"
    id = Column(Integer, primary_key=True, index=True)
    pelapor_id = Column(Integer, ForeignKey("pelapor.id"))
    kecamatan = Column(String)
    keluhan_teks_bebas = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class TriaseAI(Base):
    __tablename__ = "triase_ai"
    id = Column(Integer, primary_key=True, index=True)
    laporan_id = Column(Integer, ForeignKey("laporan_mentah.id"))
    kategori_dinas = Column(String)
    urgensi = Column(String)
    status_json = Column(String)
    waktu_disposisi = Column(DateTime(timezone=True), onupdate=func.now())
