"""Comprehensive Amorty Cafe Admin Dashboard with full CRUD features."""
import reflex as rx
from typing import List, Dict, Optional
from datetime import datetime, date
import json

# Sample data storage (in production, this would be database)
sample_data = {
    "customers": [
        {"ID_Customer": "CUS1", "Nama_Customer": "John Doe", "Kontak_Customer": "081234567890"},
        {"ID_Customer": "CUS2", "Nama_Customer": "Jane Smith", "Kontak_Customer": "081234567891"},
        {"ID_Customer": "CUS3", "Nama_Customer": "Bob Wilson", "Kontak_Customer": "081234567892"},
    ],
    "karyawan": [
        {"ID_Karyawan": "KAR1", "Nama_Karyawan": "Ahmad Saputra", "Tanggal_Masuk": "01-01-2023", "Gaji": 3500000},
        {"ID_Karyawan": "KAR2", "Nama_Karyawan": "Siti Nurhaliza", "Tanggal_Masuk": "15-02-2023", "Gaji": 3200000},
    ],
    "meja": [
        {"ID_Meja": "MJ1", "Nomor_Meja": 1, "Status_Meja": "AVAILABLE", "ID_Karyawan": "KAR1"},
        {"ID_Meja": "MJ2", "Nomor_Meja": 2, "Status_Meja": "DIPESAN", "ID_Karyawan": "KAR2"},
        {"ID_Meja": "MJ3", "Nomor_Meja": 3, "Status_Meja": "TERPAKAI", "ID_Karyawan": "KAR1"},
    ],
    "menu": [
        {"ID_Menu": "MN1", "Nama_Menu": "Nasi Goreng", "Harga_Menu": 25000, "Kategori": "Makanan"},
        {"ID_Menu": "MN2", "Nama_Menu": "Es Teh Manis", "Harga_Menu": 8000, "Kategori": "Minuman"},
        {"ID_Menu": "MN3", "Nama_Menu": "Ayam Bakar", "Harga_Menu": 35000, "Kategori": "Makanan"},
    ],
    "pesanan": [
        {"ID_Pesanan": "PES1", "ID_Customer": "CUS1", "ID_Karyawan": "KAR1", "Waktu_Pesanan": "01-12-2024 14:30", "ID_Menu": "MN1", "ID_Meja": "MJ1"},
    ],
    "transaksi": [
        {"ID_Transaksi": "TRX1", "ID_Pesanan": "PES1", "Total_Harga": 25000, "Tanggal_Transaksi": "01-12-2024", "ID_Karyawan": "KAR1"},
    ],
    "pembayaran": [
        {"ID_Pembayaran": "PB1", "ID_Pesanan": "PES1", "ID_Transaksi": "TRX1", "ID_Karyawan": "KAR1", "Metode_Pembayaran": "Cash", "Jumlah_Bayar": 25000, "Tanggal_Pembayaran": "01-12-2024"},
    ],
    "reservasi": [
        {"ID_Reservasi": "RSV1", "ID_Customer": "CUS1", "ID_Meja": "MJ2", "ID_Karyawan": "KAR1", "Tanggal_Reservasi": "02-12-2024", "Waktu_Mulai": "15:00", "Waktu_Selesai": "17:00", "Status_Reservasi": "CONFIRMED"},
    ]
}

class AdminState(rx.State):
    """Admin dashboard state management."""
    is_logged_in: bool = False
    current_page: str = "login"
    username: str = ""
    password: str = ""
    customer_id: str = ""
    error_message: str = ""
    
    # Active tab for admin dashboard
    active_tab: str = "dashboard"
    
    # Data storage
    data: Dict = sample_data
    
    # Modal states
    show_add_modal: bool = False
    show_edit_modal: bool = False
    current_edit_item: Dict = {}
    current_table: str = ""
    
    # Form states for each table
    # Customer form
    customer_nama: str = ""
    customer_kontak: str = ""
    
    # Karyawan form
    karyawan_nama: str = ""
    karyawan_tanggal: str = ""
    karyawan_gaji: str = ""
    
    # Meja form
    meja_nomor: str = ""
    meja_status: str = "AVAILABLE"
    meja_karyawan: str = ""
    
    # Menu form
    menu_nama: str = ""
    menu_harga: str = ""
    menu_kategori: str = "Makanan"
    
    # Pesanan form
    pesanan_customer: str = ""
    pesanan_karyawan: str = ""
    pesanan_menu: str = ""
    pesanan_meja: str = ""
    
    # Transaksi form
    transaksi_pesanan: str = ""
    transaksi_total: str = ""
    transaksi_karyawan: str = ""
    
    # Pembayaran form
    pembayaran_pesanan: str = ""
    pembayaran_transaksi: str = ""
    pembayaran_karyawan: str = ""
    pembayaran_metode: str = "Cash"
    pembayaran_jumlah: str = ""
    
    # Reservasi form
    reservasi_customer: str = ""
    reservasi_meja: str = ""
    reservasi_karyawan: str = ""
    reservasi_tanggal: str = ""
    reservasi_mulai: str = ""
    reservasi_selesai: str = ""
    reservasi_status: str = "PENDING"
    
    def admin_login(self):
        """Handle admin login."""
        if self.username == "admin" and self.password == "admin":
            self.is_logged_in = True
            self.current_page = "admin"
            self.error_message = ""
        else:
            self.error_message = "Username atau password admin salah!"
    
    def customer_login(self):
        """Handle customer login."""
        if self.customer_id and self.customer_id.startswith("CUS"):
            self.is_logged_in = True
            self.current_page = "customer"
            self.error_message = ""
        else:
            self.error_message = "Customer ID tidak valid! Gunakan format CUS1, CUS2, dll."
    
    def logout(self):
        """Handle logout."""
        self.is_logged_in = False
        self.current_page = "login"
        self.username = ""
        self.password = ""
        self.customer_id = ""
        self.error_message = ""
        self.active_tab = "dashboard"
    
    def set_active_tab(self, tab: str):
        """Set active tab."""
        self.active_tab = tab
        self.close_modals()
    
    def generate_id(self, table: str) -> str:
        """Generate new ID for table."""
        prefixes = {
            "customers": "CUS",
            "karyawan": "KAR", 
            "meja": "MJ",
            "menu": "MN",
            "pesanan": "PES",
            "transaksi": "TRX",
            "pembayaran": "PB",
            "reservasi": "RSV"
        }
        
        prefix = prefixes.get(table, "ID")
        existing_ids = [item.get(f"ID_{table[:-1].title()}" if table != "karyawan" else "ID_Karyawan", "") 
                       for item in self.data[table]]
        
        max_num = 0
        for id_str in existing_ids:
            if id_str.startswith(prefix):
                try:
                    num = int(id_str[len(prefix):])
                    max_num = max(max_num, num)
                except:
                    pass
        
        return f"{prefix}{max_num + 1}"
    
    def show_add_form(self, table: str):
        """Show add form modal."""
        self.current_table = table
        self.show_add_modal = True
        self.clear_form_fields()
    
    def show_edit_form(self, table: str, item: Dict):
        """Show edit form modal."""
        self.current_table = table
        self.current_edit_item = item
        self.show_edit_modal = True
        self.populate_form_fields(item)
    
    def close_modals(self):
        """Close all modals."""
        self.show_add_modal = False
        self.show_edit_modal = False
        self.current_edit_item = {}
        self.clear_form_fields()
    
    def clear_form_fields(self):
        """Clear all form fields."""
        self.customer_nama = ""
        self.customer_kontak = ""
        self.karyawan_nama = ""
        self.karyawan_tanggal = ""
        self.karyawan_gaji = ""
        self.meja_nomor = ""
        self.meja_status = "AVAILABLE"
        self.meja_karyawan = ""
        self.menu_nama = ""
        self.menu_harga = ""
        self.menu_kategori = "Makanan"
        self.pesanan_customer = ""
        self.pesanan_karyawan = ""
        self.pesanan_menu = ""
        self.pesanan_meja = ""
        self.transaksi_pesanan = ""
        self.transaksi_total = ""
        self.transaksi_karyawan = ""
        self.pembayaran_pesanan = ""
        self.pembayaran_transaksi = ""
        self.pembayaran_karyawan = ""
        self.pembayaran_metode = "Cash"
        self.pembayaran_jumlah = ""
        self.reservasi_customer = ""
        self.reservasi_meja = ""
        self.reservasi_karyawan = ""
        self.reservasi_tanggal = ""
        self.reservasi_mulai = ""
        self.reservasi_selesai = ""
        self.reservasi_status = "PENDING"
    
    def populate_form_fields(self, item: Dict):
        """Populate form fields with item data."""
        table = self.current_table
        
        if table == "customers":
            self.customer_nama = item.get("Nama_Customer", "")
            self.customer_kontak = item.get("Kontak_Customer", "")
        elif table == "karyawan":
            self.karyawan_nama = item.get("Nama_Karyawan", "")
            self.karyawan_tanggal = item.get("Tanggal_Masuk", "")
            self.karyawan_gaji = str(item.get("Gaji", ""))
        elif table == "meja":
            self.meja_nomor = str(item.get("Nomor_Meja", ""))
            self.meja_status = item.get("Status_Meja", "AVAILABLE")
            self.meja_karyawan = item.get("ID_Karyawan", "")
        elif table == "menu":
            self.menu_nama = item.get("Nama_Menu", "")
            self.menu_harga = str(item.get("Harga_Menu", ""))
            self.menu_kategori = item.get("Kategori", "Makanan")
        elif table == "pesanan":
            self.pesanan_customer = item.get("ID_Customer", "")
            self.pesanan_karyawan = item.get("ID_Karyawan", "")
            self.pesanan_menu = item.get("ID_Menu", "")
            self.pesanan_meja = item.get("ID_Meja", "")
        elif table == "transaksi":
            self.transaksi_pesanan = item.get("ID_Pesanan", "")
            self.transaksi_total = str(item.get("Total_Harga", ""))
            self.transaksi_karyawan = item.get("ID_Karyawan", "")
        elif table == "pembayaran":
            self.pembayaran_pesanan = item.get("ID_Pesanan", "")
            self.pembayaran_transaksi = item.get("ID_Transaksi", "")
            self.pembayaran_karyawan = item.get("ID_Karyawan", "")
            self.pembayaran_metode = item.get("Metode_Pembayaran", "Cash")
            self.pembayaran_jumlah = str(item.get("Jumlah_Bayar", ""))
        elif table == "reservasi":
            self.reservasi_customer = item.get("ID_Customer", "")
            self.reservasi_meja = item.get("ID_Meja", "")
            self.reservasi_karyawan = item.get("ID_Karyawan", "")
            self.reservasi_tanggal = item.get("Tanggal_Reservasi", "")
            self.reservasi_mulai = item.get("Waktu_Mulai", "")
            self.reservasi_selesai = item.get("Waktu_Selesai", "")
            self.reservasi_status = item.get("Status_Reservasi", "PENDING")
    
    def add_item(self):
        """Add new item to current table."""
        table = self.current_table
        new_item = {}
        
        if table == "customers":
            new_item = {
                "ID_Customer": self.generate_id(table),
                "Nama_Customer": self.customer_nama,
                "Kontak_Customer": self.customer_kontak
            }
        elif table == "karyawan":
            new_item = {
                "ID_Karyawan": self.generate_id(table),
                "Nama_Karyawan": self.karyawan_nama,
                "Tanggal_Masuk": self.karyawan_tanggal,
                "Gaji": float(self.karyawan_gaji) if self.karyawan_gaji else 0
            }
        elif table == "meja":
            new_item = {
                "ID_Meja": self.generate_id(table),
                "Nomor_Meja": int(self.meja_nomor) if self.meja_nomor else 0,
                "Status_Meja": self.meja_status,
                "ID_Karyawan": self.meja_karyawan
            }
        elif table == "menu":
            new_item = {
                "ID_Menu": self.generate_id(table),
                "Nama_Menu": self.menu_nama,
                "Harga_Menu": float(self.menu_harga) if self.menu_harga else 0,
                "Kategori": self.menu_kategori
            }
        elif table == "pesanan":
            new_item = {
                "ID_Pesanan": self.generate_id(table),
                "ID_Customer": self.pesanan_customer,
                "ID_Karyawan": self.pesanan_karyawan,
                "Waktu_Pesanan": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "ID_Menu": self.pesanan_menu,
                "ID_Meja": self.pesanan_meja
            }
        elif table == "transaksi":
            new_item = {
                "ID_Transaksi": self.generate_id(table),
                "ID_Pesanan": self.transaksi_pesanan,
                "Total_Harga": float(self.transaksi_total) if self.transaksi_total else 0,
                "Tanggal_Transaksi": datetime.now().strftime("%d-%m-%Y"),
                "ID_Karyawan": self.transaksi_karyawan
            }
        elif table == "pembayaran":
            new_item = {
                "ID_Pembayaran": self.generate_id(table),
                "ID_Pesanan": self.pembayaran_pesanan,
                "ID_Transaksi": self.pembayaran_transaksi,
                "ID_Karyawan": self.pembayaran_karyawan,
                "Metode_Pembayaran": self.pembayaran_metode,
                "Jumlah_Bayar": float(self.pembayaran_jumlah) if self.pembayaran_jumlah else 0,
                "Tanggal_Pembayaran": datetime.now().strftime("%d-%m-%Y")
            }
        elif table == "reservasi":
            new_item = {
                "ID_Reservasi": self.generate_id(table),
                "ID_Customer": self.reservasi_customer,
                "ID_Meja": self.reservasi_meja,
                "ID_Karyawan": self.reservasi_karyawan,
                "Tanggal_Reservasi": self.reservasi_tanggal,
                "Waktu_Mulai": self.reservasi_mulai,
                "Waktu_Selesai": self.reservasi_selesai,
                "Status_Reservasi": self.reservasi_status
            }
        
        self.data[table].append(new_item)
        self.close_modals()
    
    def update_item(self):
        """Update existing item."""
        table = self.current_table
        id_field = f"ID_{table[:-1].title()}" if table != "karyawan" else "ID_Karyawan"
        item_id = self.current_edit_item.get(id_field)
        
        # Find and update item
        for i, item in enumerate(self.data[table]):
            if item.get(id_field) == item_id:
                if table == "customers":
                    self.data[table][i].update({
                        "Nama_Customer": self.customer_nama,
                        "Kontak_Customer": self.customer_kontak
                    })
                elif table == "karyawan":
                    self.data[table][i].update({
                        "Nama_Karyawan": self.karyawan_nama,
                        "Tanggal_Masuk": self.karyawan_tanggal,
                        "Gaji": float(self.karyawan_gaji) if self.karyawan_gaji else 0
                    })
                elif table == "meja":
                    self.data[table][i].update({
                        "Nomor_Meja": int(self.meja_nomor) if self.meja_nomor else 0,
                        "Status_Meja": self.meja_status,
                        "ID_Karyawan": self.meja_karyawan
                    })
                elif table == "menu":
                    self.data[table][i].update({
                        "Nama_Menu": self.menu_nama,
                        "Harga_Menu": float(self.menu_harga) if self.menu_harga else 0,
                        "Kategori": self.menu_kategori
                    })
                # Add other table updates as needed
                break
        
        self.close_modals()
    
    def delete_item(self, table: str, item_id: str):
        """Delete item from table."""
        id_field = f"ID_{table[:-1].title()}" if table != "karyawan" else "ID_Karyawan"
        self.data[table] = [item for item in self.data[table] if item.get(id_field) != item_id]

def login_page() -> rx.Component:
    """Login page."""
    return rx.center(
        rx.vstack(
            rx.heading("🎱 Amorty Cafe Management System", size="9"),
            rx.text("Sistem Manajemen Cafe Billiard", size="5"),
            
            # Admin Login
            rx.box(
                rx.vstack(
                    rx.heading("👑 Admin Login", size="6"),
                    rx.input(
                        placeholder="Username",
                        value=AdminState.username,
                        on_change=AdminState.set_username,
                    ),
                    rx.input(
                        placeholder="Password",
                        type="password",
                        value=AdminState.password,
                        on_change=AdminState.set_password,
                    ),
                    rx.button(
                        "Login Admin",
                        on_click=AdminState.admin_login,
                        bg="blue.500",
                        color="white",
                    ),
                    spacing="3",
                ),
                p="4",
                border="1px solid #ccc",
                border_radius="md",
                m="2",
            ),
            
            rx.text("atau"),
            
            # Customer Login
            rx.box(
                rx.vstack(
                    rx.heading("👤 Customer Login", size="6"),
                    rx.input(
                        placeholder="Customer ID (contoh: CUS1)",
                        value=AdminState.customer_id,
                        on_change=AdminState.set_customer_id,
                    ),
                    rx.button(
                        "Login Customer",
                        on_click=AdminState.customer_login,
                        bg="green.500",
                        color="white",
                    ),
                    spacing="3",
                ),
                p="4",
                border="1px solid #ccc",
                border_radius="md",
                m="2",
            ),
            
            # Error message
            rx.cond(
                AdminState.error_message != "",
                rx.text(AdminState.error_message, color="red"),
            ),
            
            spacing="4",
            align="center",
        ),
        height="100vh",
    )

def create_data_table(table_name: str, data: List[Dict], headers: List[str]) -> rx.Component:
    """Create a data table component."""
    return rx.vstack(
        rx.hstack(
            rx.heading(f"Data {table_name.title()}", size="6"),
            rx.button(
                f"+ Tambah {table_name.title()}",
                on_click=lambda: AdminState.show_add_form(table_name),
                bg="green.500",
                color="white",
                size="sm"
            ),
            justify="between",
            width="100%",
            mb="4"
        ),
        
        rx.table(
            rx.thead(
                rx.tr(*[rx.th(header) for header in headers + ["Actions"]])
            ),
            rx.tbody(
                *[
                    rx.tr(
                        *[rx.td(str(item.get(header, ""))) for header in headers],
                        rx.td(
                            rx.hstack(
                                rx.button(
                                    "Edit",
                                    on_click=lambda item=item: AdminState.show_edit_form(table_name, item),
                                    bg="blue.500",
                                    color="white",
                                    size="xs"
                                ),
                                rx.button(
                                    "Delete",
                                    on_click=lambda item=item: AdminState.delete_item(
                                        table_name, 
                                        item.get(f"ID_{table_name[:-1].title()}" if table_name != "karyawan" else "ID_Karyawan")
                                    ),
                                    bg="red.500",
                                    color="white",
                                    size="xs"
                                ),
                                spacing="2"
                            )
                        )
                    )
                    for item in data
                ]
            ),
            variant="striped",
            width="100%"
        ),
        
        width="100%",
        spacing="4"
    )

def create_customer_form() -> rx.Component:
    """Create customer form."""
    return rx.vstack(
        rx.input(
            placeholder="Nama Customer",
            value=AdminState.customer_nama,
            on_change=AdminState.set_customer_nama,
        ),
        rx.input(
            placeholder="Kontak Customer",
            value=AdminState.customer_kontak,
            on_change=AdminState.set_customer_kontak,
        ),
        spacing="3",
        width="100%"
    )

def create_karyawan_form() -> rx.Component:
    """Create karyawan form."""
    return rx.vstack(
        rx.input(
            placeholder="Nama Karyawan",
            value=AdminState.karyawan_nama,
            on_change=AdminState.set_karyawan_nama,
        ),
        rx.input(
            placeholder="Tanggal Masuk (dd-mm-yyyy)",
            value=AdminState.karyawan_tanggal,
            on_change=AdminState.set_karyawan_tanggal,
        ),
        rx.input(
            placeholder="Gaji",
            type="number",
            value=AdminState.karyawan_gaji,
            on_change=AdminState.set_karyawan_gaji,
        ),
        spacing="3",
        width="100%"
    )

def create_meja_form() -> rx.Component:
    """Create meja form."""
    return rx.vstack(
        rx.input(
            placeholder="Nomor Meja",
            type="number",
            value=AdminState.meja_nomor,
            on_change=AdminState.set_meja_nomor,
        ),
        rx.select(
            ["AVAILABLE", "DIPESAN", "TERPAKAI"],
            value=AdminState.meja_status,
            on_change=AdminState.set_meja_status,
        ),
        rx.select(
            [item["ID_Karyawan"] for item in AdminState.data["karyawan"]],
            placeholder="Pilih Karyawan",
            value=AdminState.meja_karyawan,
            on_change=AdminState.set_meja_karyawan,
        ),
        spacing="3",
        width="100%"
    )

def create_menu_form() -> rx.Component:
    """Create menu form."""
    return rx.vstack(
        rx.input(
            placeholder="Nama Menu",
            value=AdminState.menu_nama,
            on_change=AdminState.set_menu_nama,
        ),
        rx.input(
            placeholder="Harga Menu",
            type="number",
            value=AdminState.menu_harga,
            on_change=AdminState.set_menu_harga,
        ),
        rx.select(
            ["Makanan", "Minuman"],
            value=AdminState.menu_kategori,
            on_change=AdminState.set_menu_kategori,
        ),
        spacing="3",
        width="100%"
    )

def create_modal(title: str, form_component: rx.Component, is_edit: bool = False) -> rx.Component:
    """Create modal component."""
    return rx.dialog_root(
        rx.dialog_content(
            rx.dialog_title(title),
            form_component,
            rx.hstack(
                rx.button(
                    "Batal",
                    on_click=AdminState.close_modals,
                    variant="outline"
                ),
                rx.button(
                    "Simpan",
                    on_click=AdminState.update_item if is_edit else AdminState.add_item,
                    bg="green.500",
                    color="white"
                ),
                justify="end",
                spacing="3",
                mt="4"
            ),
            max_width="400px"
        ),
        open=AdminState.show_edit_modal if is_edit else AdminState.show_add_modal
    )

def admin_page() -> rx.Component:
    """Admin dashboard with full CRUD features."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("👑 Admin Dashboard - Amorty Cafe", size="8"),
                rx.button("Logout", on_click=AdminState.logout),
                justify="between",
                width="100%",
                pb="4"
            ),
            
            # Tab navigation
            rx.hstack(
                rx.button(
                    "📊 Dashboard",
                    on_click=lambda: AdminState.set_active_tab("dashboard"),
                    bg="blue.500" if AdminState.active_tab == "dashboard" else "gray.200",
                    color="white" if AdminState.active_tab == "dashboard" else "black",
                    size="sm"
                ),
                rx.button(
                    "👥 Customer",
                    on_click=lambda: AdminState.set_active_tab("customers"),
                    bg="blue.500" if AdminState.active_tab == "customers" else "gray.200",
                    color="white" if AdminState.active_tab == "customers" else "black",
                    size="sm"
                ),
                rx.button(
                    "👨‍💼 Karyawan",
                    on_click=lambda: AdminState.set_active_tab("karyawan"),
                    bg="blue.500" if AdminState.active_tab == "karyawan" else "gray.200",
                    color="white" if AdminState.active_tab == "karyawan" else "black",
                    size="sm"
                ),
                rx.button(
                    "🎱 Meja",
                    on_click=lambda: AdminState.set_active_tab("meja"),
                    bg="blue.500" if AdminState.active_tab == "meja" else "gray.200",
                    color="white" if AdminState.active_tab == "meja" else "black",
                    size="sm"
                ),
                rx.button(
                    "🍽️ Menu",
                    on_click=lambda: AdminState.set_active_tab("menu"),
                    bg="blue.500" if AdminState.active_tab == "menu" else "gray.200",
                    color="white" if AdminState.active_tab == "menu" else "black",
                    size="sm"
                ),
                rx.button(
                    "📋 Pesanan",
                    on_click=lambda: AdminState.set_active_tab("pesanan"),
                    bg="blue.500" if AdminState.active_tab == "pesanan" else "gray.200",
                    color="white" if AdminState.active_tab == "pesanan" else "black",
                    size="sm"
                ),
                rx.button(
                    "💰 Transaksi",
                    on_click=lambda: AdminState.set_active_tab("transaksi"),
                    bg="blue.500" if AdminState.active_tab == "transaksi" else "gray.200",
                    color="white" if AdminState.active_tab == "transaksi" else "black",
                    size="sm"
                ),
                rx.button(
                    "💳 Pembayaran",
                    on_click=lambda: AdminState.set_active_tab("pembayaran"),
                    bg="blue.500" if AdminState.active_tab == "pembayaran" else "gray.200",
                    color="white" if AdminState.active_tab == "pembayaran" else "black",
                    size="sm"
                ),
                rx.button(
                    "📅 Reservasi",
                    on_click=lambda: AdminState.set_active_tab("reservasi"),
                    bg="blue.500" if AdminState.active_tab == "reservasi" else "gray.200",
                    color="white" if AdminState.active_tab == "reservasi" else "black",
                    size="sm"
                ),
                spacing="2",
                wrap="wrap",
                mb="6"
            ),
            
            # Content based on active tab
            rx.cond(
                AdminState.active_tab == "dashboard",
                rx.vstack(
                    rx.text("📊 Dashboard Overview", size="6", weight="bold"),
                    rx.grid(
                        rx.box(f"👥 Total Customer: {len(AdminState.data['customers'])}", p="4", bg="blue.100", border_radius="md"),
                        rx.box(f"👨‍💼 Total Karyawan: {len(AdminState.data['karyawan'])}", p="4", bg="green.100", border_radius="md"),
                        rx.box(f"🎱 Total Meja: {len(AdminState.data['meja'])}", p="4", bg="yellow.100", border_radius="md"),
                        rx.box(f"🍽️ Total Menu: {len(AdminState.data['menu'])}", p="4", bg="purple.100", border_radius="md"),
                        rx.box(f"📋 Total Pesanan: {len(AdminState.data['pesanan'])}", p="4", bg="red.100", border_radius="md"),
                        rx.box(f"💰 Total Transaksi: {len(AdminState.data['transaksi'])}", p="4", bg="orange.100", border_radius="md"),
                        rx.box(f"💳 Total Pembayaran: {len(AdminState.data['pembayaran'])}", p="4", bg="pink.100", border_radius="md"),
                        rx.box(f"📅 Total Reservasi: {len(AdminState.data['reservasi'])}", p="4", bg="cyan.100", border_radius="md"),
                        columns="4",
                        spacing="4",
                        width="100%"
                    ),
                    spacing="6",
                    width="100%"
                )
            ),
            
            rx.cond(
                AdminState.active_tab == "customers",
                create_data_table("customers", AdminState.data["customers"], ["ID_Customer", "Nama_Customer", "Kontak_Customer"])
            ),
            
            rx.cond(
                AdminState.active_tab == "karyawan",
                create_data_table("karyawan", AdminState.data["karyawan"], ["ID_Karyawan", "Nama_Karyawan", "Tanggal_Masuk", "Gaji"])
            ),
            
            rx.cond(
                AdminState.active_tab == "meja",
                create_data_table("meja", AdminState.data["meja"], ["ID_Meja", "Nomor_Meja", "Status_Meja", "ID_Karyawan"])
            ),
            
            rx.cond(
                AdminState.active_tab == "menu",
                create_data_table("menu", AdminState.data["menu"], ["ID_Menu", "Nama_Menu", "Harga_Menu", "Kategori"])
            ),
            
            rx.cond(
                AdminState.active_tab == "pesanan",
                create_data_table("pesanan", AdminState.data["pesanan"], ["ID_Pesanan", "ID_Customer", "ID_Karyawan", "Waktu_Pesanan", "ID_Menu", "ID_Meja"])
            ),
            
            rx.cond(
                AdminState.active_tab == "transaksi",
                create_data_table("transaksi", AdminState.data["transaksi"], ["ID_Transaksi", "ID_Pesanan", "Total_Harga", "Tanggal_Transaksi", "ID_Karyawan"])
            ),
            
            rx.cond(
                AdminState.active_tab == "pembayaran",
                create_data_table("pembayaran", AdminState.data["pembayaran"], ["ID_Pembayaran", "ID_Pesanan", "ID_Transaksi", "ID_Karyawan", "Metode_Pembayaran", "Jumlah_Bayar", "Tanggal_Pembayaran"])
            ),
            
            rx.cond(
                AdminState.active_tab == "reservasi",
                create_data_table("reservasi", AdminState.data["reservasi"], ["ID_Reservasi", "ID_Customer", "ID_Meja", "ID_Karyawan", "Tanggal_Reservasi", "Waktu_Mulai", "Waktu_Selesai", "Status_Reservasi"])
            ),
            
            spacing="6",
            width="100%",
            p="6"
        ),
        
        # Modals
        create_modal("Tambah Customer", create_customer_form(), False),
        create_modal("Edit Customer", create_customer_form(), True),
        create_modal("Tambah Karyawan", create_karyawan_form(), False),
        create_modal("Edit Karyawan", create_karyawan_form(), True),
        create_modal("Tambah Meja", create_meja_form(), False),
        create_modal("Edit Meja", create_meja_form(), True),
        create_modal("Tambah Menu", create_menu_form(), False),
        create_modal("Edit Menu", create_menu_form(), True),
        
        max_width="1200px",
    )

def customer_page() -> rx.Component:
    """Customer dashboard."""
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("👤 Customer Dashboard - Amorty Cafe", size="8"),
                rx.button("Logout", on_click=AdminState.logout),
                justify="between",
                width="100%",
            ),
            rx.text(f"Selamat datang, Customer {AdminState.customer_id}!", size="5"),
            rx.text("Dashboard customer akan dikembangkan selanjutnya.", size="4"),
            
            # Simple menu
            rx.hstack(
                rx.box("🍽️ Lihat Menu", p="4", bg="blue.100"),
                rx.box("🎱 Status Meja", p="4", bg="green.100"),
                rx.box("📋 Riwayat Pesanan", p="4", bg="yellow.100"),
                spacing="4",
            ),
            
            spacing="6",
            p="6",
        )
    )

def index():
    """Main page that shows login or dashboard based on state."""
    return rx.cond(
        AdminState.is_logged_in,
        rx.cond(
            AdminState.current_page == "admin",
            admin_page(),
            customer_page(),
        ),
        login_page(),
    )

# Create app
app = rx.App()
app.add_page(index, route="/")
