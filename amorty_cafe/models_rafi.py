"""Database models matching Rafi's Oracle schema."""
import reflex as rx
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Status Enums
class StatusMeja(Enum):
    AVAILABLE = "AVAILABLE"
    DIPESAN = "DIPESAN"
    TERPAKAI = "TERPAKAI"

class StatusReservasi(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED" 
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class KategoriMenu(Enum):
    MAKANAN = "Makanan"
    MINUMAN = "Minuman"

class MetodePembayaran(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    DIGITAL_WALLET = "Digital Wallet"

# Main Tables
class Customer(rx.Model, table=True):
    """Customer table - Tabel pelanggan."""
    __tablename__ = "CUSTOMER"
    
    ID_Customer: str = rx.Field(primary_key=True)  # Format: CUS1, CUS2, etc.
    Nama_Customer: str
    Kontak_Customer: str

class Karyawan(rx.Model, table=True):
    """Karyawan table - Tabel karyawan."""
    __tablename__ = "KARYAWAN"
    
    ID_Karyawan: str = rx.Field(primary_key=True)  # Format: KAR1, KAR2, etc.
    Nama_Karyawan: str
    Tanggal_Masuk: datetime
    Gaji: float

class Meja(rx.Model, table=True):
    """Meja table - Tabel meja billiard."""
    __tablename__ = "MEJA"
    
    ID_Meja: str = rx.Field(primary_key=True)  # Format: MJ1, MJ2, etc.
    Nomor_Meja: int
    Status_Meja: str = "AVAILABLE"  # AVAILABLE, DIPESAN, TERPAKAI
    ID_Karyawan: Optional[str] = None  # FK to Karyawan

class Menu(rx.Model, table=True):
    """Menu table - Tabel menu cafe."""
    __tablename__ = "MENU"
    
    ID_Menu: str = rx.Field(primary_key=True)  # Format: MN1, MN2, etc.
    Nama_Menu: str
    Harga_Menu: float
    Kategori: str  # Makanan, Minuman

class Pesanan(rx.Model, table=True):
    """Pesanan table - Tabel pesanan."""
    __tablename__ = "PESANAN"
    
    ID_Pesanan: str = rx.Field(primary_key=True)  # Format: PES1, PES2, etc.
    ID_Customer: str  # FK to Customer
    ID_Karyawan: Optional[str] = None  # FK to Karyawan
    Waktu_Pesanan: datetime
    ID_Menu: str  # FK to Menu
    ID_Meja: str  # FK to Meja

class Transaksi(rx.Model, table=True):
    """Transaksi table - Tabel transaksi."""
    __tablename__ = "TRANSAKSI"
    
    ID_Transaksi: str = rx.Field(primary_key=True)  # Format: TRX1, TRX2, etc.
    ID_Pesanan: str  # FK to Pesanan
    Total_Harga: float
    Tanggal_Transaksi: datetime
    ID_Karyawan: str  # FK to Karyawan

class Pembayaran(rx.Model, table=True):
    """Pembayaran table - Tabel pembayaran."""
    __tablename__ = "PEMBAYARAN"
    
    ID_Pembayaran: str = rx.Field(primary_key=True)  # Format: PB1, PB2, etc.
    ID_Pesanan: str  # FK to Pesanan
    ID_Transaksi: str  # FK to Transaksi
    ID_Karyawan: str  # FK to Karyawan
    Metode_Pembayaran: str
    Jumlah_Bayar: float
    Tanggal_Pembayaran: datetime

class Reservasi(rx.Model, table=True):
    """Reservasi table - Tabel reservasi meja."""
    __tablename__ = "RESERVASI"
    
    ID_Reservasi: str = rx.Field(primary_key=True)  # Format: RSV1, RSV2, etc.
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
    import re
    from .database import get_oracle_session
    
    if not prefix:
        prefix = get_prefix_for_table(table_name)
    
    session = get_oracle_session()
    if not session:
        return f"{prefix}1"
    
    try:
        # Get the model class based on table name
        model_map = {
            'CUSTOMER': Customer,
            'KARYAWAN': Karyawan,
            'MEJA': Meja,
            'MENU': Menu,
            'PESANAN': Pesanan,
            'TRANSAKSI': Transaksi,
            'PEMBAYARAN': Pembayaran,
            'RESERVASI': Reservasi,
        }
        
        model_class = model_map.get(table_name.upper())
        if not model_class:
            return f"{prefix}1"
        
        # Get the primary key field name
        id_field = list(model_class.__table__.primary_key.columns)[0].name
        
        # Query to get max number from existing IDs
        query = f"""
            SELECT MAX(CAST(REGEXP_SUBSTR({id_field}, '\\d+') AS NUMBER)) 
            FROM {table_name} 
            WHERE {id_field} LIKE :prefix
        """
        
        result = session.execute(rx.text(query), {"prefix": f"{prefix}%"}).scalar()
        next_number = 1 if result is None else int(result) + 1
        
        return f"{prefix}{next_number}"
        
    except Exception as e:
        print(f"Error generating ID for {table_name}: {e}")
        return f"{prefix}1"
    finally:
        session.close()
