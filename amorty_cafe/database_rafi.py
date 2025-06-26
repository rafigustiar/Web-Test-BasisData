"""Enhanced database setup with Oracle client initialization for Rafi's system."""
import cx_Oracle
import os
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import reflex as rx
from .models_rafi import *
from datetime import datetime
import json

class OracleDatabaseRafi:
    """Oracle database connection and management for Rafi's system."""
    
    def __init__(self):
        self.oracle_lib_dir = os.getenv("ORACLE_LIB_DIR", r"C:\Users\Rafi Gustiar\Oracle\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")
        self.connection_string = self._get_oracle_connection_string()
        self.engine = None
        self.session_maker = None
        self._init_oracle_client()
    
    def _init_oracle_client(self):
        """Initialize Oracle client library."""
        try:
            if os.path.exists(self.oracle_lib_dir):
                cx_Oracle.init_oracle_client(lib_dir=self.oracle_lib_dir)
                print(f"✅ Oracle client initialized with lib_dir: {self.oracle_lib_dir}")
            else:
                print(f"⚠️  Oracle lib directory not found: {self.oracle_lib_dir}")
                print("Trying to initialize without lib_dir...")
                cx_Oracle.init_oracle_client()
        except cx_Oracle.Error as e:
            print(f"❌ Oracle client initialization error: {e}")
        except Exception as e:
            print(f"Oracle client may already be initialized: {e}")
    
    def _get_oracle_connection_string(self) -> str:
        """Get Oracle connection string from environment variables."""
        host = os.getenv("ORACLE_HOST", "localhost")
        port = os.getenv("ORACLE_PORT", "1521")
        service_name = os.getenv("ORACLE_SERVICE_NAME", "xe")
        username = os.getenv("ORACLE_USERNAME", "AMORTY")
        password = os.getenv("ORACLE_PASSWORD", "sys")
        
        # Oracle DSN format for cx_Oracle
        dsn = f"{host}:{port}/{service_name}"
        return f"oracle+cx_oracle://{username}:{password}@{dsn}"
    
    def test_connection(self) -> bool:
        """Test Oracle connection using cx_Oracle directly."""
        try:
            host = os.getenv("ORACLE_HOST", "localhost")
            port = os.getenv("ORACLE_PORT", "1521")
            service_name = os.getenv("ORACLE_SERVICE_NAME", "xe")
            username = os.getenv("ORACLE_USERNAME", "AMORTY")
            password = os.getenv("ORACLE_PASSWORD", "sys")
            
            dsn = f"{host}:{port}/{service_name}"
            
            connection = cx_Oracle.connect(
                user=username,
                password=password,
                dsn=dsn
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT 'Connection Test' FROM DUAL")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            print(f"✅ Oracle connection test successful: {result[0]}")
            return True
            
        except cx_Oracle.Error as e:
            print(f"❌ Oracle connection test failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def connect(self):
        """Connect to Oracle database using SQLAlchemy."""
        try:
            self.engine = create_engine(
                self.connection_string,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.session_maker = sessionmaker(bind=self.engine)
            print("✅ SQLAlchemy Oracle database connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Oracle database: {e}")
            return False
    
    def create_tables(self):
        """Create all tables in Oracle database."""
        try:
            # Test connection first
            if not self.test_connection():
                print("❌ Cannot create tables - connection test failed")
                return False
            
            # Create tables using Reflex models
            rx.Model.metadata.create_all(self.engine)
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def get_session(self):
        """Get database session."""
        if self.session_maker:
            return self.session_maker()
        return None

# Global database instance
oracle_db_rafi = OracleDatabaseRafi()

def setup_database_rafi():
    """Setup database connection and create tables for Rafi's system."""
    print("🚀 Setting up Rafi's Oracle database...")
    print("=" * 50)
    
    # Test connection first
    if not oracle_db_rafi.test_connection():
        print("❌ Database setup failed - cannot connect to Oracle")
        return False
    
    success = oracle_db_rafi.connect()
    if success:
        oracle_db_rafi.create_tables()
        seed_sample_data_rafi()
        return True
    return False

def seed_sample_data_rafi():
    """Seed the database with sample data for Rafi's schema."""
    session = oracle_db_rafi.get_session()
    if not session:
        print("❌ Cannot seed data - no database session")
        return
    
    try:
        # Check if data already exists
        if session.query(Customer).first():
            print("ℹ️  Sample data already exists!")
            return
        
        # Create sample customers
        customers = [
            Customer(
                ID_Customer="CUS1",
                Nama_Customer="John Doe",
                Kontak_Customer="+62812345671"
            ),
            Customer(
                ID_Customer="CUS2", 
                Nama_Customer="Jane Smith",
                Kontak_Customer="+62812345672"
            ),
            Customer(
                ID_Customer="CUS3",
                Nama_Customer="Mike Johnson", 
                Kontak_Customer="+62812345673"
            )
        ]
        
        # Create sample karyawan
        karyawan = [
            Karyawan(
                ID_Karyawan="KAR1",
                Nama_Karyawan="Alice Brown",
                Tanggal_Masuk=datetime(2023, 1, 15),
                Gaji=4500000.0
            ),
            Karyawan(
                ID_Karyawan="KAR2",
                Nama_Karyawan="Bob Wilson",
                Tanggal_Masuk=datetime(2023, 3, 10),
                Gaji=3500000.0
            ),
            Karyawan(
                ID_Karyawan="KAR3",
                Nama_Karyawan="Carol Davis",
                Tanggal_Masuk=datetime(2023, 5, 20),
                Gaji=3000000.0
            )
        ]
        
        # Create sample meja
        meja = [
            Meja(
                ID_Meja="MJ1",
                Nomor_Meja=1,
                Status_Meja="AVAILABLE",
                ID_Karyawan="KAR1"
            ),
            Meja(
                ID_Meja="MJ2",
                Nomor_Meja=2, 
                Status_Meja="AVAILABLE",
                ID_Karyawan="KAR2"
            ),
            Meja(
                ID_Meja="MJ3",
                Nomor_Meja=3,
                Status_Meja="DIPESAN",
                ID_Karyawan="KAR3"
            ),
            Meja(
                ID_Meja="MJ4",
                Nomor_Meja=4,
                Status_Meja="AVAILABLE",
                ID_Karyawan="KAR1"
            )
        ]
        
        # Create sample menu
        menu = [
            Menu(
                ID_Menu="MN1",
                Nama_Menu="Espresso",
                Harga_Menu=15000.0,
                Kategori="Minuman"
            ),
            Menu(
                ID_Menu="MN2",
                Nama_Menu="Cappuccino", 
                Harga_Menu=20000.0,
                Kategori="Minuman"
            ),
            Menu(
                ID_Menu="MN3",
                Nama_Menu="Nasi Goreng",
                Harga_Menu=25000.0,
                Kategori="Makanan"
            ),
            Menu(
                ID_Menu="MN4",
                Nama_Menu="Sandwich Club",
                Harga_Menu=30000.0,
                Kategori="Makanan"
            )
        ]
        
        # Add all sample data
        session.add_all(customers + karyawan + meja + menu)
        session.commit()
        
        # Create sample pesanan
        pesanan = [
            Pesanan(
                ID_Pesanan="PES1",
                ID_Customer="CUS1",
                ID_Karyawan="KAR1",
                Waktu_Pesanan=datetime.now(),
                ID_Menu="MN1",
                ID_Meja="MJ1"
            ),
            Pesanan(
                ID_Pesanan="PES2",
                ID_Customer="CUS2",
                ID_Karyawan="KAR2", 
                Waktu_Pesanan=datetime.now(),
                ID_Menu="MN3",
                ID_Meja="MJ2"
            )
        ]
        
        session.add_all(pesanan)
        session.commit()
        
        print("✅ Sample data seeded successfully!")
        print(f"   - {len(customers)} customers")
        print(f"   - {len(karyawan)} karyawan")
        print(f"   - {len(meja)} meja")
        print(f"   - {len(menu)} menu items")
        print(f"   - {len(pesanan)} pesanan")
        
    except Exception as e:
        print(f"❌ Failed to seed sample data: {e}")
        session.rollback()
    finally:
        session.close()

def get_oracle_session_rafi():
    """Get Oracle database session for Rafi's system."""
    return oracle_db_rafi.get_session()

# Initialize database on import
if __name__ == "__main__":
    setup_database_rafi()
