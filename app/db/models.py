"""SQLAlchemy database models."""
# pylint: disable=too-few-public-methods, not-callable
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Uuid
from sqlalchemy.sql import func
from app.db.database import Base

class Pelapor(Base):
    """Model representing a person making a report."""
    __tablename__ = "pelapor"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = Column(String, unique=True, index=True)
    nama = Column(String)
    no_hp = Column(String)

class LaporanMentah(Base):
    """Model representing the raw report data."""
    __tablename__ = "laporan_mentah"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pelapor_id = Column(Uuid(as_uuid=True), ForeignKey("pelapor.id"))
    kecamatan = Column(String)
    keluhan_teks_bebas = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class TriaseAI(Base):
    """Model representing the AI triage results."""
    __tablename__ = "triase_ai"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    laporan_id = Column(Uuid(as_uuid=True), ForeignKey("laporan_mentah.id"))
    kategori_dinas = Column(String)
    urgensi = Column(String)
    status_json = Column(String)
    waktu_disposisi = Column(DateTime(timezone=True), onupdate=func.now())
