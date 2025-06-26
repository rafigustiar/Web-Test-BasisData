# 🎱 Amorty Cafe Management System

Sistem manajemen billiard cafe yang dibuat dengan **Python Reflex** dengan UI yang modern dan responsif.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Reflex](https://img.shields.io/badge/Reflex-Latest-purple.svg)
![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Fitur Utama

### 🔐 **Authentication & Security**

- Login/Register system dengan role-based access (Admin/Customer)
- JWT token authentication dengan bcrypt password hashing
- Session management dan security middleware

### 📊 **Dashboard Management**

- Real-time statistics dan metrics
- Interactive charts dan visualizations
- Quick actions dan shortcuts
- Recent activity tracking

### 👥 **Customer Management**

- Complete customer database dengan membership types
- Loyalty points tracking
- Customer activity history
- Advanced search dan filtering

### 🎯 **Complete Feature Set**

1. **Employee Management** - Staff scheduling & management
2. **Menu Management** - Cafe menu dengan categories
3. **Order Management** - POS system dengan real-time tracking
4. **Payment Processing** - Multi-method payment handling
5. **Reservation System** - Table booking dengan time slots
6. **Rental Management** - Real-time table usage tracking
7. **Table Management** - Billiard table status & maintenance

## 🛠️ Tech Stack

- **Framework**: [Reflex](https://reflex.dev/) - Modern Python web framework
- **Database**: Oracle Database dengan cx_Oracle driver
- **Authentication**: JWT + bcrypt encryption
- **UI**: TailwindCSS dengan dark theme
- **Icons**: Lucide React icon set
- **State Management**: Reflex built-in state system

## 🚀 Quick Start

### 1. **Clone & Setup**

```bash
git clone <repository>
cd amorty-cafe-management
```

### 2. **Automatic Setup** (Recommended)

```bash
python setup.py
```

### 3. **Manual Setup**

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dengan Oracle database credentials Anda

# Initialize database
python -c "from amorty_cafe.database import setup_database; setup_database()"

# Run aplikasi
reflex run
```

## 🗄️ Database Setup

### **Oracle Database Configuration**

#### Option A: Oracle XE (Development)

```bash
# Download Oracle XE atau gunakan Docker
docker run -d -p 1521:1521 --name oracle-xe -e ORACLE_PWD=yourpassword gvenzl/oracle-xe:latest
```

#### Option B: Existing Oracle Database

```sql
-- Connect sebagai DBA
sqlplus sys/password@localhost:1521/XE as sysdba

-- Create user untuk aplikasi
CREATE USER amorty_user IDENTIFIED BY amorty_pass;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER TO amorty_user;
GRANT UNLIMITED TABLESPACE TO amorty_user;
```

### **Environment Configuration**

```bash
# Edit .env file
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XE
ORACLE_USERNAME=amorty_user
ORACLE_PASSWORD=amorty_pass
```

## 🎮 Usage

### **Default Accounts**

```
👑 Admin Account:
   Username: admin
   Password: admin123

👤 Customer Account:
   Username: customer1
   Password: customer123
```

### **Application Access**

- **Local Development**: http://localhost:3000
- **Admin Dashboard**: Full management access
- **Customer Portal**: Limited customer-specific features

## 📁 Project Structure

```
amorty_cafe/
├── 📁 components/          # Reusable UI components
│   ├── layout.py          # Main layout & navigation
│   └── __init__.py
├── 📁 pages/              # Application pages
│   ├── login.py           # Authentication pages
│   ├── signup.py
│   ├── dashboard.py       # Main dashboard
│   ├── customers.py       # Customer management
│   └── __init__.py
├── models.py              # Database models
├── auth.py                # Authentication logic
├── database.py            # Oracle database setup
└── amorty_cafe.py         # Main application

📄 Root Files:
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── rxconfig.py           # Reflex configuration
├── setup.py              # Auto setup script
└── .env.example          # Environment template
```

## 🎨 UI Features

### **Dark Theme Design**

- Modern glassmorphism effects
- Gradient backgrounds dengan subtle animations
- Responsive grid layouts
- Interactive hover states dan transitions

### **Component Library**

- Reusable form components
- Data tables dengan sorting & filtering
- Modal dialogs untuk CRUD operations
- Loading states dan error handling

### **Mobile Responsive**

- Mobile-first design approach
- Collapsible navigation menu
- Touch-friendly interfaces
- Optimized layouts untuk semua screen sizes

## 🔧 Development

### **Adding New Features**

```python
# 1. Create new page
# amorty_cafe/pages/new_feature.py
def new_feature_page():
    return layout(
        rx.heading("New Feature")
    )

# 2. Add route di amorty_cafe.py
app.add_page(new_feature_page, route="/new-feature")
```

### **Database Models**

```python
# Add new model di models.py
class NewModel(rx.Model, table=True):
    name: str
    created_at: datetime = datetime.now()

# Update database
python -c "from amorty_cafe.database import oracle_db; oracle_db.create_tables()"
```

### **Development Commands**

```bash
# Development server dengan hot reload
reflex run

# Production build
reflex export

# Database reset
python -c "from amorty_cafe.database import setup_database; setup_database()"

# Clear cache
reflex clean
```

## 🚀 Deployment

### **Local Production**

```bash
reflex run --env prod --port 8000
```

### **Docker Deployment**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 3000

CMD ["reflex", "run", "--env", "prod"]
```

## 📊 Database Schema

### **Core Tables**

- **users** - Authentication & user roles
- **customers** - Customer information & memberships
- **employees** - Staff management
- **menu_cafe** - Menu items & pricing
- **billiard_table** - Table information & status

### **Transaction Tables**

- **orders** & **order_items** - Order management
- **payments** - Payment processing
- **reservations** - Table bookings
- **rental_transactions** - Active table rentals

## 🔍 API Endpoints

### **Authentication**

- `POST /api/auth/login` - User authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/logout` - Session termination

### **Management APIs**

- Customer CRUD operations
- Employee management
- Menu item management
- Order processing workflow
- Payment handling
- Reservation system
- Real-time rental tracking

## 🐛 Troubleshooting

### **Common Issues**

#### Oracle Connection Problems

```bash
# Check Oracle service
lsnrctl status

# Verify user permissions
sqlplus amorty_user/amorty_pass@localhost:1521/XE
```

#### Reflex Issues

```bash
# Clear cache dan reinstall
reflex clean
pip install --force-reinstall reflex
```

#### Permission Errors

```bash
# On Linux/Mac, install Oracle drivers
sudo apt-get install libaio1 libaio-dev
# Download Oracle Instant Client
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

Distributed under MIT License. See `LICENSE` for more information.

## 🎯 Roadmap

### **Phase 1 - Core Features** ✅

- [x] Authentication system
- [x] Customer management
- [x] Basic dashboard
- [x] Database integration

### **Phase 2 - Advanced Features** 🚧

- [ ] Employee management
- [ ] Menu management
- [ ] Order processing
- [ ] Payment system

### **Phase 3 - Enterprise Features** 📋

- [ ] Real-time notifications
- [ ] Advanced reporting
- [ ] Multi-branch support
- [ ] Mobile app API
- [ ] Advanced analytics

## 💡 Features in Detail

### **Customer Management**

- Complete customer profiles dengan contact information
- Membership tiers (Regular, VIP, Premium)
- Loyalty points system
- Purchase history tracking
- Advanced search dan filtering capabilities

### **Dashboard Analytics**

- Real-time revenue tracking
- Table occupancy rates
- Popular menu items
- Customer engagement metrics
- Staff performance indicators

### **Security Features**

- Role-based access control (RBAC)
- Session timeout handling
- Password strength requirements
- Audit logging untuk sensitive operations
- Data encryption in transit

## 📞 Support

Untuk support dan pertanyaan:

- 📧 Email: support@amorty.cafe
- 📱 Phone: (0341) 487789
- 💬 GitHub Issues: [Create an issue](../../issues)

---

**Dibuat dengan ❤️ menggunakan Python Reflex**

_Professional billiard cafe management system dengan modern UI dan comprehensive features._
