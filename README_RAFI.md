# 🎱 Amorty Cafe Management System - Versi Rafi

Konversi aplikasi Tkinter menjadi modern web application menggunakan **Reflex (Python)** dengan design yang sama persis seperti gambar dashboard.

![Amorty Dashboard](https://cdn.builder.io/api/v1/image/assets%2F420a2dccf542446cabbce903b3e093cd%2F8bd7535bd4994d80ad50666ebd69ef58?format=webp&width=800)

## 🎯 Fitur Utama

### 🔐 **Sistem Login**

- **Admin Login**: username=`admin`, password=`admin`
- **Customer Login**: menggunakan ID Customer dari database (CUS1, CUS2, dst.)
- **Role-based access** dengan UI yang berbeda untuk Admin dan Customer

### 👑 **Admin Dashboard**

- **Complete CRUD operations** untuk semua tabel:
  - CUSTOMER (Pelanggan)
  - KARYAWAN (Staff)
  - MEJA (Meja Billiard)
  - MENU (Menu Cafe)
  - PESANAN (Orders)
  - PEMBAYARAN (Payments)
  - RESERVASI (Reservations)
  - TRANSAKSI (Transactions)

### 👤 **Customer Dashboard**

- **Daftar Menu**: Lihat dan pesan menu cafe
- **Daftar Meja**: Lihat status meja billiard
- **Pesanan Saya**: Track pesanan yang telah dibuat
- **Order System**: Pesan menu dengan pemilihan meja

## 🛠️ Tech Stack

- **Frontend**: Reflex (Python web framework)
- **Database**: Oracle Database dengan cx_Oracle
- **UI**: TailwindCSS dengan dark theme modern
- **Icons**: Lucide React icons
- **Authentication**: Custom role-based system

## 🚀 Instalasi & Setup

### 1. **Persiapan Sistem**

```bash
# Clone repository
git clone <repository>
cd amorty-cafe-rafi

# Install Python dependencies
pip install -r requirements.txt
```

### 2. **Setup Oracle Database**

Pastikan Oracle Database sudah running dan buat user:

```sql
-- Connect as system user
sqlplus sys/password@localhost:1521/xe as sysdba

-- Create user AMORTY
CREATE USER AMORTY IDENTIFIED BY sys;
GRANT DBA TO AMORTY;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO AMORTY;
GRANT UNLIMITED TABLESPACE TO AMORTY;
```

### 3. **Setup Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit .env file dengan konfigurasi Oracle Anda
# ORACLE_HOST=localhost
# ORACLE_PORT=1521
# ORACLE_SERVICE_NAME=xe
# ORACLE_USERNAME=AMORTY
# ORACLE_PASSWORD=sys
# ORACLE_LIB_DIR=C:\Users\Rafi Gustiar\Oracle\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8
```

### 4. **Initialize Database**

```bash
# Setup database dan seed sample data
python main_rafi.py --setup-db
```

### 5. **Run Application**

```bash
# Start aplikasi
python main_rafi.py

# Atau menggunakan Reflex langsung
reflex run
```

Aplikasi akan berjalan di: **http://localhost:3000**

## 🎮 Cara Penggunaan

### 🔐 **Login**

#### Admin Login:

- Username: `admin`
- Password: `admin`
- Akses: Full admin dashboard dengan CRUD semua tabel

#### Customer Login:

- ID Customer: `CUS1`, `CUS2`, `CUS3` (dari sample data)
- Password: Tidak diperlukan
- Akses: Customer dashboard untuk order menu

### 👑 **Admin Features**

1. **Tab Management**: Pilih tabel yang ingin dikelola
2. **Add Data**: Klik tombol "Tambah" untuk menambah record baru
3. **Edit Data**: Klik icon edit pada baris data
4. **Delete Data**: Klik icon delete dengan konfirmasi
5. **Auto ID Generation**: ID otomatis dengan prefix (CUS1, KAR1, MJ1, dst.)

### 👤 **Customer Features**

1. **Daftar Menu**: Browse menu cafe dengan harga
2. **Order Menu**:
   - Pilih menu yang diinginkan
   - Pilih meja yang tersedia (status AVAILABLE)
   - Submit pesanan
3. **Track Pesanan**: Lihat riwayat pesanan di tab "Pesanan Saya"

## 📊 Database Schema

### **Tabel Utama**

```sql
-- CUSTOMER
ID_Customer (PK) | Nama_Customer | Kontak_Customer

-- KARYAWAN
ID_Karyawan (PK) | Nama_Karyawan | Tanggal_Masuk | Gaji

-- MEJA
ID_Meja (PK) | Nomor_Meja | Status_Meja | ID_Karyawan (FK)

-- MENU
ID_Menu (PK) | Nama_Menu | Harga_Menu | Kategori

-- PESANAN
ID_Pesanan (PK) | ID_Customer (FK) | ID_Karyawan (FK) |
Waktu_Pesanan | ID_Menu (FK) | ID_Meja (FK)

-- PEMBAYARAN
ID_Pembayaran (PK) | ID_Pesanan (FK) | ID_Transaksi (FK) |
ID_Karyawan (FK) | Metode_Pembayaran | Jumlah_Bayar | Tanggal_Pembayaran

-- RESERVASI
ID_Reservasi (PK) | ID_Customer (FK) | ID_Meja (FK) | ID_Karyawan (FK) |
Tanggal_Reservasi | Waktu_Mulai | Waktu_Selesai | Status_Reservasi

-- TRANSAKSI
ID_Transaksi (PK) | ID_Pesanan (FK) | Total_Harga |
Tanggal_Transaksi | ID_Karyawan (FK)
```

### **Status Values**

- **Status_Meja**: AVAILABLE, DIPESAN, TERPAKAI
- **Status_Reservasi**: PENDING, CONFIRMED, CANCELLED, COMPLETED
- **Kategori Menu**: Makanan, Minuman
- **Metode_Pembayaran**: Cash, Credit Card, Debit Card, Digital Wallet

## 🎨 UI Features

### **Design System**

- **Dark Theme**: Gradient background dengan glassmorphism effects
- **Modern Cards**: Rounded corners dengan backdrop blur
- **Color Coding**: Status indicators dengan warna yang konsisten
- **Responsive**: Mobile-friendly dengan adaptive layouts

### **Interactive Elements**

- **Smooth Transitions**: Hover effects dan animations
- **Modal Dialogs**: Form input dengan validation
- **Real-time Updates**: Data refresh otomatis setelah operasi CRUD
- **Loading States**: Visual feedback untuk operasi async

## 🔧 Development

### **Project Structure**

```
amorty_cafe/
├── models_rafi.py          # Database models sesuai schema Rafi
├── database_rafi.py        # Oracle setup dan connection management
├── pages/
│   ├── login_rafi.py       # Enhanced login dengan role selection
│   ├── admin_dashboard.py  # Complete admin CRUD interface
│   └── customer_dashboard.py # Customer ordering interface
├── components/
│   └── layout.py          # Shared layout components
├── auth.py                # Authentication logic
└── amorty_cafe.py         # Main app dengan routing

Root Files:
├── main_rafi.py           # Enhanced entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README_RAFI.md        # Documentation ini
```

### **Key Features Implementation**

#### **Auto ID Generation**

```python
def generate_custom_id(table_name: str) -> str:
    prefix = get_prefix_for_table(table_name)  # CUS, KAR, MJ, dll.
    # Logic untuk generate ID berikutnya: CUS1, CUS2, dst.
```

#### **Foreign Key Handling**

```python
def get_fk_options(field: str) -> List[str]:
    # Otomatis populate dropdown dengan data dari tabel terkait
    # Contoh: ID_Karyawan dropdown diisi dari tabel KARYAWAN
```

#### **Date Handling**

```python
# Konversi format tanggal antara form input dan database
# Support format dd-mm-yyyy untuk user input
```

## 🚀 Production Deployment

### **Environment Setup**

```bash
# Production environment variables
export ORACLE_HOST=your-prod-host
export ORACLE_USERNAME=AMORTY_PROD
export ORACLE_PASSWORD=your-secure-password
export ORACLE_LIB_DIR=/path/to/oracle/instantclient
```

### **Run Production**

```bash
# Production mode
reflex run --env prod --port 8000
```

## 🐛 Troubleshooting

### **Oracle Connection Issues**

```bash
# Check Oracle service
lsnrctl status

# Test connection
sqlplus AMORTY/sys@localhost:1521/xe

# Verify instant client
echo $ORACLE_LIB_DIR
ls $ORACLE_LIB_DIR
```

### **Common Errors**

1. **"Oracle client library not found"**

   - Download Oracle Instant Client
   - Set ORACLE_LIB_DIR di .env file

2. **"ORA-12541: TNS:no listener"**

   - Start Oracle service
   - Check port 1521 terbuka

3. **"ORA-01017: invalid username/password"**
   - Verify kredensial di .env
   - Check user permissions

## 📈 Future Enhancements

- [ ] Real-time notifications untuk order status
- [ ] Advanced reporting dan analytics
- [ ] Print receipts untuk pembayaran
- [ ] Multi-language support (ID/EN)
- [ ] Mobile app integration
- [ ] Advanced table management
- [ ] Inventory management
- [ ] Staff scheduling system

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Create Pull Request

## 📄 License

MIT License - See LICENSE file for details.

---

**Dikembangkan dengan ❤️ menggunakan Python Reflex**

_Konversi lengkap dari Tkinter ke modern web application dengan UI yang sama persis seperti design "Amorty & Cafe"._

### 📞 Support

Untuk pertanyaan dan dukungan:

- 📧 Email: support@amorty.cafe
- 📱 Telp: (0341) 487789
- 💬 GitHub Issues: [Create an issue](../../issues)
