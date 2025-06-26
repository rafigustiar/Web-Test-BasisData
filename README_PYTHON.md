# Amorty Cafe Management System (Python/Reflex)

Sistem manajemen billiard cafe yang dibuat dengan Reflex (Python) dengan tampilan UI yang sama persis seperti versi React.

## 🚀 Fitur Utama

### 👥 **Manajemen Pengguna**

- **Authentication System**: Login/Register untuk Admin dan Customer
- **Role-based Access**: Admin dan Customer memiliki akses berbeda
- **Security**: JWT tokens dan password hashing dengan bcrypt

### 📊 **Dashboard Management**

- **Real-time Statistics**: Total customers, revenue, table availability
- **Recent Activity**: Orders terbaru dan reservasi mendatang
- **Quick Actions**: Shortcut untuk operasi umum

### 🎯 **Fitur Lengkap**

1. **Customer Management** - Kelola pelanggan dan membership
2. **Employee Management** - Kelola staff dan jadwal kerja
3. **Menu Management** - Kelola menu cafe dengan kategori
4. **Order Management** - Sistem pemesanan dengan item selection
5. **Payment Management** - Proses pembayaran multi-method
6. **Reservation Management** - Booking meja billiard
7. **Rental Management** - Track penggunaan meja real-time
8. **Table Management** - Kelola meja billiard dan status

## 🛠️ Tech Stack

- **Framework**: [Reflex](https://reflex.dev/) (Python web framework)
- **Database**: Oracle Database dengan cx_Oracle
- **Authentication**: JWT + bcrypt
- **UI**: TailwindCSS (sama persis dengan versi React)
- **Icons**: Lucide React icons

## 📋 Requirements

- Python 3.8+
- Oracle Database 11g+ atau Oracle XE
- Oracle Instant Client

## 🚀 Instalasi

### 1. Clone dan Setup

```bash
git clone <repository>
cd amorty-cafe-python
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Oracle Database

**Option A: Oracle XE (Recommended untuk development)**

```bash
# Download dan install Oracle XE dari Oracle website
# Atau menggunakan Docker:
docker run -d -p 1521:1521 --name oracle-xe -e ORACLE_PWD=yourpassword gvenzl/oracle-xe:latest
```

**Option B: Oracle Database Existing**

- Pastikan Oracle Database sudah running
- Buat user baru untuk aplikasi

### 4. Setup Environment

```bash
# Copy file environment
cp .env.example .env

# Edit file .env sesuai konfigurasi Oracle Anda
# ORACLE_HOST=localhost
# ORACLE_PORT=1521
# ORACLE_SERVICE_NAME=XE
# ORACLE_USERNAME=amorty_user
# ORACLE_PASSWORD=amorty_pass
```

### 5. Setup Database Schema

```bash
# Buat user dan schema di Oracle
sqlplus sys/yourpassword@localhost:1521/XE as sysdba

CREATE USER amorty_user IDENTIFIED BY amorty_pass;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER TO amorty_user;
GRANT UNLIMITED TABLESPACE TO amorty_user;
```

### 6. Initialize Database

```bash
# Jalankan setup database
python -c "from amorty_cafe.database import setup_database; setup_database()"
```

### 7. Run Application

```bash
# Development mode
reflex run

# Production mode
reflex run --env prod
```

Aplikasi akan berjalan di `http://localhost:3000`

## 🔐 Default Login

### Admin Account

- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full management dashboard

### Customer Account

- **Username**: `customer1`
- **Password**: `customer123`
- **Access**: Customer dashboard

## 🗂️ Struktur Project

```
amorty_cafe/
├── __init__.py
├── amorty_cafe.py          # Main app dengan routing
├── models.py               # Database models
├── auth.py                 # Authentication logic
├── database.py             # Oracle database setup
├── components/
│   └── layout.py           # Layout dan navigation
├── pages/
│   ��── login.py            # Halaman login
│   ├── signup.py           # Halaman registrasi
│   ├── dashboard.py        # Dashboard utama
│   ├── customers.py        # Management customers
│   ├── employees.py        # Management employees
│   ├── menu.py             # Management menu
│   ├── orders.py           # Management orders
│   ├── payments.py         # Management payments
│   ├── reservations.py     # Management reservations
│   ├── rentals.py          # Management rentals
│   └── tables.py           # Management tables
└── utils/
    └── helpers.py          # Helper functions
```

## 🔧 Konfigurasi Oracle

### Untuk Production Environment

```bash
# Environment variables
export ORACLE_HOST=your-oracle-host
export ORACLE_PORT=1521
export ORACLE_SERVICE_NAME=your-service-name
export ORACLE_USERNAME=your-username
export ORACLE_PASSWORD=your-password
```

### Connection String Format

```python
oracle+cx_oracle://username:password@host:port/?service_name=service_name
```

## 📊 Database Schema

Database menggunakan model yang sama dengan versi React:

- **Users** - Authentication dan roles
- **Customers** - Data pelanggan
- **Employees** - Data karyawan
- **MenuCafe** - Menu items
- **BilliardTable** - Data meja billiard
- **Orders & OrderItems** - Sistem pemesanan
- **Payments** - Transaksi pembayaran
- **Reservations** - Booking meja
- **RentalTransactions** - Sewa meja aktif

## 🎨 UI Components

UI menggunakan design system yang sama dengan versi React:

### Dark Theme

- Background: Gradient dark slate
- Cards: Glass morphism effect
- Colors: Blue, Green, Purple, Orange accents

### Responsive Design

- Mobile-first approach
- Hamburger menu untuk mobile
- Grid layout yang adaptif

### Interactive Elements

- Hover effects dan transitions
- Loading states
- Form validation
- Real-time updates

## 🚀 Deployment

### Local Production

```bash
# Build untuk production
reflex export --frontend-only

# Atau jalankan dengan production settings
reflex run --env prod --port 8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 3000

CMD ["reflex", "run", "--env", "prod"]
```

## 🔧 Development

### Adding New Pages

```python
# 1. Buat file di amorty_cafe/pages/new_page.py
def new_page():
    return layout(
        rx.heading("New Page")
    )

# 2. Add route di amorty_cafe.py
app.add_page(new_page, route="/new-page")
```

### Adding New Models

```python
# 1. Tambah model di models.py
class NewModel(rx.Model, table=True):
    name: str
    created_at: datetime = datetime.now()

# 2. Update database
python -c "from amorty_cafe.database import oracle_db; oracle_db.create_tables()"
```

## 🐛 Troubleshooting

### Oracle Connection Issues

```bash
# Check Oracle service status
lsnrctl status

# Check if user exists
sqlplus / as sysdba
SELECT username FROM all_users WHERE username = 'AMORTY_USER';
```

### Reflex Issues

```bash
# Clear Reflex cache
reflex clean

# Reinstall dependencies
pip install --force-reinstall reflex
```

## 📝 API Documentation

### Authentication Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration
- `POST /api/auth/logout` - User logout

### Management Endpoints

- Customer CRUD operations
- Employee management
- Menu management
- Order processing
- Payment handling
- Reservation system
- Rental tracking

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push ke branch
5. Create Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🎯 Next Features

- [ ] Real-time notifications
- [ ] Advanced reporting
- [ ] Email integration
- [ ] Mobile app API
- [ ] Advanced analytics
- [ ] Multi-branch support

---

**Dibuat dengan ❤️ menggunakan Reflex dan Oracle Database**

Konversi dari React ke Python dengan UI yang identik dan fitur lengkap untuk manajemen billiard cafe.
