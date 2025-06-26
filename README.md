# 🎱 Amorty Cafe Management System

Sistem manajemen cafe billiard modern menggunakan Python Reflex dengan database Oracle.

## 🚀 Cara Menjalankan Aplikasi

### Metode 1: Menggunakan Script Startup (Paling Mudah)

```bash
python run_app.py
```

### Metode 2: Menggunakan Perintah Reflex Langsung

```bash
reflex run
```

### Metode 3: Menggunakan Main Script

```bash
python main_rafi.py
```

## 📋 Prerequisites

1. **Python 3.8+** sudah terinstall
2. **Dependencies** sudah diinstall:

   ```bash
   pip install -r requirements.txt
   ```

3. **Oracle Database** tersetup dan running
4. **Oracle Instant Client** terinstall (untuk cx_Oracle)

## ⚙️ Konfigurasi

1. **Copy file .env.example ke .env**:

   ```bash
   cp .env.example .env
   ```

2. **Edit .env file** sesuai dengan konfigurasi database Oracle Anda:
   ```
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE_NAME=xe
   ORACLE_USERNAME=AMORTY
   ORACLE_PASSWORD=your_password
   ORACLE_LIB_DIR=path_to_oracle_instant_client
   ```

## 🔐 Login Credentials

- **Admin**:

  - Username: `admin`
  - Password: `admin`

- **Customer**:
  - Gunakan ID Customer dari database (contoh: CUS1, CUS2, CUS3)

## 🌐 Akses Aplikasi

Setelah aplikasi berjalan, buka browser dan kunjungi:
**http://localhost:3000**

## 📊 Fitur Utama

### Admin Dashboard:

- ✅ Manajemen Customer (Pelanggan)
- ✅ Manajemen Karyawan
- ✅ Manajemen Menu Cafe
- ✅ Manajemen Meja Billiard
- ✅ Manajemen Pesanan
- ✅ Manajemen Pembayaran
- ✅ Manajemen Reservasi
- ✅ Manajemen Transaksi

### Customer Dashboard:

- ✅ Melihat Menu
- ✅ Membuat Pesanan
- ✅ Melihat Status Meja
- ✅ Riwayat Pesanan

## 🛠️ Troubleshooting

### Error: Module 'reflex' not found

```bash
pip install reflex
```

### Error: Oracle connection failed

1. Pastikan Oracle Database sudah running
2. Periksa konfigurasi di file .env
3. Pastikan Oracle Instant Client sudah terinstall

### Error: Port already in use

- Matikan aplikasi lain yang menggunakan port 3000 atau 8000
- Atau ubah port di file rxconfig.py

## 📁 Struktur Project

```
amorty_cafe/
├── amorty_cafe/          # Main application package
│   ├── models_rafi.py    # Database models
│   ├── database_rafi.py  # Database connection
│   ├── auth.py          # Authentication system
│   ├── pages/           # Web pages
│   └── components/      # Reusable components
├── rxconfig.py          # Reflex configuration
├── run_app.py          # Simple startup script
├── main_rafi.py        # Main entry point
└── requirements.txt    # Python dependencies
```

## 💡 Tips

1. **Pertama kali menjalankan**: Gunakan `python run_app.py` untuk setup otomatis
2. **Development**: Gunakan `reflex run` untuk hot reload
3. **Production**: Gunakan `reflex run --env prod`

---

Dibuat dengan ❤️ untuk Amorty Cafe & Billiard
