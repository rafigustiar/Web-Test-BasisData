"""Comprehensive admin dashboard with all CRUD operations."""
import reflex as rx
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from ..components.layout import layout
from ..auth import AuthState, require_admin
from ..models_rafi import *
import json

class AdminDashboardState(rx.State):
    """Admin dashboard state management."""
    current_tab: str = "CUSTOMER"
    
    # Data storage for each table
    customers: List[Dict[str, Any]] = []
    karyawan: List[Dict[str, Any]] = []
    meja: List[Dict[str, Any]] = []
    menu: List[Dict[str, Any]] = []
    pesanan: List[Dict[str, Any]] = []
    pembayaran: List[Dict[str, Any]] = []
    reservasi: List[Dict[str, Any]] = []
    transaksi: List[Dict[str, Any]] = []
    
    # Form states
    is_dialog_open: bool = False
    editing_item: Dict[str, Any] = {}
    form_data: Dict[str, Any] = {}
    selected_id: str = ""
    
    # Table definitions
    table_configs = {
        'CUSTOMER': {
            'fields': ['ID_Customer', 'Nama_Customer', 'Kontak_Customer'],
            'model': Customer
        },
        'KARYAWAN': {
            'fields': ['ID_Karyawan', 'Nama_Karyawan', 'Tanggal_Masuk', 'Gaji'],
            'model': Karyawan
        },
        'MEJA': {
            'fields': ['ID_Meja', 'Nomor_Meja', 'Status_Meja', 'ID_Karyawan'],
            'model': Meja
        },
        'MENU': {
            'fields': ['ID_Menu', 'Nama_Menu', 'Harga_Menu', 'Kategori'],
            'model': Menu
        },
        'PESANAN': {
            'fields': ['ID_Pesanan', 'ID_Customer', 'ID_Karyawan', 'Waktu_Pesanan', 'ID_Menu', 'ID_Meja'],
            'model': Pesanan
        },
        'PEMBAYARAN': {
            'fields': ['ID_Pembayaran', 'ID_Pesanan', 'ID_Transaksi', 'ID_Karyawan', 'Metode_Pembayaran', 'Jumlah_Bayar', 'Tanggal_Pembayaran'],
            'model': Pembayaran
        },
        'RESERVASI': {
            'fields': ['ID_Reservasi', 'ID_Customer', 'ID_Meja', 'ID_Karyawan', 'Tanggal_Reservasi', 'Waktu_Mulai', 'Waktu_Selesai', 'Status_Reservasi'],
            'model': Reservasi
        },
        'TRANSAKSI': {
            'fields': ['ID_Transaksi', 'ID_Pesanan', 'Total_Harga', 'Tanggal_Transaksi', 'ID_Karyawan'],
            'model': Transaksi
        }
    }
    
    def set_current_tab(self, tab: str):
        """Set current active tab."""
        self.current_tab = tab
        self.load_table_data(tab)
    
    async def load_table_data(self, table_name: str):
        """Load data for specific table."""
        config = self.table_configs.get(table_name)
        if not config:
            return
            
        try:
            with rx.session() as session:
                model_class = config['model']
                items = session.query(model_class).all()
                
                data = []
                for item in items:
                    item_dict = {}
                    for field in config['fields']:
                        value = getattr(item, field, None)
                        if isinstance(value, datetime):
                            item_dict[field] = value.strftime('%d-%m-%Y')
                        else:
                            item_dict[field] = value
                    data.append(item_dict)
                
                # Store in appropriate state variable
                setattr(self, table_name.lower(), data)
                
        except Exception as e:
            print(f"Error loading {table_name}: {e}")
    
    def open_add_dialog(self):
        """Open dialog for adding new item."""
        fields = self.table_configs[self.current_tab]['fields']
        self.editing_item = {}
        self.form_data = {field: "" for field in fields[1:]}  # Skip ID field
        self.is_dialog_open = True
    
    def open_edit_dialog(self, item: Dict[str, Any]):
        """Open dialog for editing item."""
        fields = self.table_configs[self.current_tab]['fields']
        self.editing_item = item
        self.form_data = {field: str(item.get(field, "")) for field in fields[1:]}
        self.selected_id = item.get(fields[0], "")
        self.is_dialog_open = True
    
    def close_dialog(self):
        """Close dialog."""
        self.is_dialog_open = False
        self.editing_item = {}
        self.form_data = {}
        self.selected_id = ""
    
    def set_form_field(self, field: str, value: str):
        """Set form field value."""
        self.form_data[field] = value
    
    async def save_item(self):
        """Save item to database."""
        try:
            config = self.table_configs[self.current_tab]
            model_class = config['model']
            fields = config['fields']
            
            with rx.session() as session:
                if self.editing_item:
                    # Update existing item
                    item = session.query(model_class).filter(
                        getattr(model_class, fields[0]) == self.selected_id
                    ).first()
                    
                    if item:
                        for field in fields[1:]:
                            value = self.form_data.get(field, "")
                            if "tanggal" in field.lower() or "waktu" in field.lower():
                                if value:
                                    try:
                                        value = datetime.strptime(value, "%d-%m-%Y")
                                    except ValueError:
                                        value = datetime.strptime(value, "%Y-%m-%d")
                            elif field in ["Gaji", "Harga_Menu", "Jumlah_Bayar", "Total_Harga"]:
                                value = float(value) if value else 0.0
                            elif field in ["Nomor_Meja"]:
                                value = int(value) if value else 0
                            
                            setattr(item, field, value)
                else:
                    # Create new item
                    new_id = generate_custom_id(self.current_tab)
                    
                    item_data = {fields[0]: new_id}
                    for field in fields[1:]:
                        value = self.form_data.get(field, "")
                        if "tanggal" in field.lower() or "waktu" in field.lower():
                            if value:
                                try:
                                    value = datetime.strptime(value, "%d-%m-%Y")
                                except ValueError:
                                    value = datetime.strptime(value, "%Y-%m-%d")
                            else:
                                value = datetime.now()
                        elif field in ["Gaji", "Harga_Menu", "Jumlah_Bayar", "Total_Harga"]:
                            value = float(value) if value else 0.0
                        elif field in ["Nomor_Meja"]:
                            value = int(value) if value else 0
                        
                        item_data[field] = value
                    
                    new_item = model_class(**item_data)
                    session.add(new_item)
                
                session.commit()
                self.close_dialog()
                await self.load_table_data(self.current_tab)
                
        except Exception as e:
            print(f"Error saving item: {e}")
    
    async def delete_item(self, item_id: str):
        """Delete item from database."""
        try:
            config = self.table_configs[self.current_tab]
            model_class = config['model']
            fields = config['fields']
            
            with rx.session() as session:
                item = session.query(model_class).filter(
                    getattr(model_class, fields[0]) == item_id
                ).first()
                
                if item:
                    session.delete(item)
                    session.commit()
                    await self.load_table_data(self.current_tab)
                    
        except Exception as e:
            print(f"Error deleting item: {e}")
    
    def get_fk_options(self, field: str) -> List[str]:
        """Get foreign key options for dropdown."""
        fk_map = {
            "ID_Karyawan": self.karyawan,
            "ID_Customer": self.customers,
            "ID_Meja": self.meja,
            "ID_Menu": self.menu,
            "ID_Pesanan": self.pesanan,
            "ID_Transaksi": self.transaksi,
        }
        
        data = fk_map.get(field, [])
        field_key = field
        return [item.get(field_key, "") for item in data if item.get(field_key)]

def table_tab_button(tab_name: str, label: str) -> rx.Component:
    """Create tab button."""
    return rx.button(
        label,
        on_click=lambda: AdminDashboardState.set_current_tab(tab_name),
        class_name=f"""
            px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium
            {
                'bg-blue-600 text-white shadow-lg' if AdminDashboardState.current_tab == tab_name 
                else 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }
        """,
        variant="outline"
    )

def form_field(field_name: str, field_type: str = "text") -> rx.Component:
    """Create form field based on field name and type."""
    
    # Special handling for specific fields
    if field_name == "Kategori" and AdminDashboardState.current_tab == "MENU":
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.select(
                ["Makanan", "Minuman"],
                value=AdminDashboardState.form_data.get(field_name, "Makanan"),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    elif field_name == "Status_Meja":
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.select(
                ["AVAILABLE", "DIPESAN", "TERPAKAI"],
                value=AdminDashboardState.form_data.get(field_name, "AVAILABLE"),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    elif field_name == "Status_Reservasi":
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.select(
                ["PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"],
                value=AdminDashboardState.form_data.get(field_name, "PENDING"),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    elif field_name == "Metode_Pembayaran":
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.select(
                ["Cash", "Credit Card", "Debit Card", "Digital Wallet"],
                value=AdminDashboardState.form_data.get(field_name, "Cash"),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    elif any(fk in field_name for fk in ["ID_Karyawan", "ID_Customer", "ID_Meja", "ID_Menu", "ID_Pesanan", "ID_Transaksi"]):
        # Foreign key fields
        options = AdminDashboardState.get_fk_options(field_name)
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.select(
                options,
                value=AdminDashboardState.form_data.get(field_name, ""),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    elif "tanggal" in field_name.lower() or "waktu" in field_name.lower():
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.input(
                type="date",
                value=AdminDashboardState.form_data.get(field_name, ""),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )
    else:
        # Regular text/number fields
        input_type = "number" if field_name in ["Gaji", "Harga_Menu", "Jumlah_Bayar", "Total_Harga", "Nomor_Meja"] else "text"
        return rx.vstack(
            rx.text(field_name, class_name="text-sm font-medium text-slate-300"),
            rx.input(
                type=input_type,
                placeholder=f"Masukkan {field_name}",
                value=AdminDashboardState.form_data.get(field_name, ""),
                on_change=lambda value: AdminDashboardState.set_form_field(field_name, value),
                class_name="bg-slate-700 border-slate-600 text-white"
            ),
            class_name="space-y-1"
        )

def data_form() -> rx.Component:
    """Data form dialog."""
    return rx.cond(
        AdminDashboardState.is_dialog_open,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                AdminDashboardState.editing_item,
                                f"Edit {AdminDashboardState.current_tab}",
                                f"Tambah {AdminDashboardState.current_tab}"
                            ),
                            class_name="text-white text-xl font-semibold"
                        ),
                        rx.button(
                            rx.icon(tag="x", size=20),
                            on_click=AdminDashboardState.close_dialog,
                            class_name="text-slate-400 hover:text-white bg-transparent border-none",
                            variant="ghost"
                        ),
                        class_name="flex justify-between items-center w-full"
                    ),
                    
                    rx.vstack(
                        *[
                            form_field(field) 
                            for field in AdminDashboardState.table_configs[AdminDashboardState.current_tab]['fields'][1:]
                        ],
                        class_name="space-y-4 w-full max-h-96 overflow-y-auto"
                    ),
                    
                    rx.hstack(
                        rx.button(
                            "Batal",
                            on_click=AdminDashboardState.close_dialog,
                            class_name="border-slate-600 text-slate-300 hover:bg-slate-700",
                            variant="outline"
                        ),
                        rx.button(
                            rx.cond(
                                AdminDashboardState.editing_item,
                                "Update",
                                "Tambah"
                            ),
                            on_click=AdminDashboardState.save_item,
                            class_name="bg-blue-600 hover:bg-blue-700 text-white"
                        ),
                        class_name="flex justify-end space-x-2 pt-4"
                    ),
                    
                    class_name="space-y-6"
                ),
                class_name="bg-slate-800 border-slate-700 text-white max-w-2xl w-full rounded-lg p-8 max-h-screen overflow-y-auto"
            ),
            class_name="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        )
    )

def data_table() -> rx.Component:
    """Data table component."""
    current_data = getattr(AdminDashboardState, AdminDashboardState.current_tab.lower())
    fields = AdminDashboardState.table_configs[AdminDashboardState.current_tab]['fields']
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(f"Data {AdminDashboardState.current_tab}", class_name="text-2xl font-bold text-white"),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="plus", size=16),
                            rx.text("Tambah"),
                            class_name="flex items-center space-x-2"
                        ),
                        on_click=AdminDashboardState.open_add_dialog,
                        class_name="bg-blue-600 hover:bg-blue-700 text-white"
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="refresh_cw", size=16),
                            rx.text("Refresh"),
                            class_name="flex items-center space-x-2"
                        ),
                        on_click=lambda: AdminDashboardState.load_table_data(AdminDashboardState.current_tab),
                        class_name="bg-slate-600 hover:bg-slate-700 text-white"
                    ),
                    class_name="flex items-center space-x-2"
                ),
                class_name="flex justify-between items-center w-full"
            ),
            
            rx.box(
                rx.table(
                    rx.thead(
                        rx.tr(
                            *[rx.th(field, class_name="text-slate-300 font-semibold text-left py-3 px-4") for field in fields],
                            rx.th("Actions", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                            class_name="bg-slate-700/30 border-slate-700"
                        )
                    ),
                    rx.tbody(
                        rx.foreach(
                            current_data,
                            lambda item: rx.tr(
                                *[rx.td(item[field], class_name="text-slate-200 py-3 px-4") for field in fields],
                                rx.td(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon(tag="edit", size=16),
                                            on_click=lambda: AdminDashboardState.open_edit_dialog(item),
                                            class_name="h-8 w-8 p-0 text-slate-400 hover:text-yellow-400 bg-transparent border-none",
                                            variant="ghost"
                                        ),
                                        rx.button(
                                            rx.icon(tag="trash_2", size=16),
                                            on_click=lambda: AdminDashboardState.delete_item(item[fields[0]]),
                                            class_name="h-8 w-8 p-0 text-slate-400 hover:text-red-400 bg-transparent border-none",
                                            variant="ghost"
                                        ),
                                        class_name="flex items-center space-x-2"
                                    ),
                                    class_name="text-slate-200 py-3 px-4"
                                ),
                                class_name="border-slate-700 hover:bg-slate-700/20 transition-colors"
                            )
                        )
                    ),
                    class_name="w-full"
                ),
                class_name="rounded-md border border-slate-700 overflow-x-auto"
            ),
            
            class_name="space-y-4"
        ),
        class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
    )

@require_admin
def admin_dashboard_page() -> rx.Component:
    """Admin dashboard page."""
    
    # Load initial data
    AdminDashboardState.load_table_data(AdminDashboardState.current_tab)
    
    return layout(
        rx.vstack(
            rx.vstack(
                rx.heading("Admin Dashboard", class_name="text-3xl font-bold text-white"),
                rx.text("Sistem Manajemen Cafe Billiard", class_name="text-slate-400"),
                class_name="text-center space-y-2"
            ),
            
            # Tab Navigation
            rx.box(
                rx.hstack(
                    table_tab_button("CUSTOMER", "Customer"),
                    table_tab_button("KARYAWAN", "Karyawan"),
                    table_tab_button("MEJA", "Meja"),
                    table_tab_button("MENU", "Menu"),
                    table_tab_button("PESANAN", "Pesanan"),
                    table_tab_button("PEMBAYARAN", "Pembayaran"),
                    table_tab_button("RESERVASI", "Reservasi"),
                    table_tab_button("TRANSAKSI", "Transaksi"),
                    class_name="flex flex-wrap gap-2"
                ),
                class_name="bg-slate-800/50 border-slate-700 rounded-lg p-4"
            ),
            
            # Data Table
            data_table(),
            
            # Form Dialog
            data_form(),
            
            class_name="space-y-6"
        )
    )
