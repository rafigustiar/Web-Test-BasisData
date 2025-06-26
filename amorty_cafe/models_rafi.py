"""Database models matching Rafi's Oracle schema."""
import reflex as rx
from typing import Optional
from datetime import datetime

# Main Tables
class Customer(rx.Model, table=True):
    """Customer table - Tabel pelanggan."""
    __tablename__ = "CUSTOMER"

    ID_Customer: str
    Nama_Customer: str
    Kontak_Customer: str

class Karyawan(rx.Model, table=True):
    """Karyawan table - Tabel karyawan."""
    __tablename__ = "KARYAWAN"

    ID_Karyawan: str
    Nama_Karyawan: str
    Tanggal_Masuk: datetime
    Gaji: float

class Meja(rx.Model, table=True):
    """Meja table - Tabel meja billiard."""
    __tablename__ = "MEJA"

    ID_Meja: str
    Nomor_Meja: int
    Status_Meja: str = "AVAILABLE"  # AVAILABLE, DIPESAN, TERPAKAI
    ID_Karyawan: Optional[str] = None  # FK to Karyawan

class Menu(rx.Model, table=True):
    """Menu table - Tabel menu cafe."""
    __tablename__ = "MENU"

    ID_Menu: str
    Nama_Menu: str
    Harga_Menu: float
    Kategori: str  # Makanan, Minuman

class Pesanan(rx.Model, table=True):
    """Pesanan table - Tabel pesanan."""
    __tablename__ = "PESANAN"

    ID_Pesanan: str
    ID_Customer: str  # FK to Customer
    ID_Karyawan: Optional[str] = None  # FK to Karyawan
    Waktu_Pesanan: datetime
    ID_Menu: str  # FK to Menu
    ID_Meja: str  # FK to Meja

class Transaksi(rx.Model, table=True):
    """Transaksi table - Tabel transaksi."""
    __tablename__ = "TRANSAKSI"

    ID_Transaksi: str
    ID_Pesanan: str  # FK to Pesanan
    Total_Harga: float
    Tanggal_Transaksi: datetime
    ID_Karyawan: str  # FK to Karyawan

class Pembayaran(rx.Model, table=True):
    """Pembayaran table - Tabel pembayaran."""
    __tablename__ = "PEMBAYARAN"

    ID_Pembayaran: str
    ID_Pesanan: str  # FK to Pesanan
    ID_Transaksi: str  # FK to Transaksi
    ID_Karyawan: str  # FK to Karyawan
    Metode_Pembayaran: str
    Jumlah_Bayar: float
    Tanggal_Pembayaran: datetime

class Reservasi(rx.Model, table=True):
    """Reservasi table - Tabel reservasi meja."""
    __tablename__ = "RESERVASI"

    ID_Reservasi: str
    ID_Customer: str  # FK to Customer
    ID_Meja: str  # FK to Meja
    ID_Karyawan: str  # FK to Karyawan
    Tanggal_Reservasi: datetime
    Waktu_Mulai: str  # Format: HH:MM
    Waktu_Selesai: str  # Format: HH:MM
    Status_Reservasi: str = "PENDING"  # PENDING, CONFIRMED, CANCELLED, COMPLETED

# Utility functions for ID generation
def get_prefix_for_table(table_name: str) -> str:
    """Get prefix for table ID generation."""
    return {
        'CUSTOMER': 'CUS',
        'MEJA': 'MJ',
        'MENU': 'MN',
        'PESANAN': 'PES',
        'PEMBAYARAN': 'PB',
        'RESERVASI': 'RSV',
        'TRANSAKSI': 'TRX',
        'KARYAWAN': 'KAR',
    }.get(table_name.upper(), 'ID')

def generate_custom_id(table_name: str, prefix: str = None) -> str:
    """Generate custom ID for table."""
    if not prefix:
        prefix = get_prefix_for_table(table_name)
    
    # Simple ID generation - can be enhanced with database query
    import random
    return f"{prefix}{random.randint(1, 9999)}"

# Status options for dropdowns
STATUS_MEJA_OPTIONS = ["AVAILABLE", "DIPESAN", "TERPAKAI"]
STATUS_RESERVASI_OPTIONS = ["PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"]
KATEGORI_MENU_OPTIONS = ["Makanan", "Minuman"]
METODE_PEMBAYARAN_OPTIONS = ["Cash", "Credit Card", "Debit Card", "Digital Wallet"]
