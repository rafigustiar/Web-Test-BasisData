"""Customer dashboard with menu ordering and table reservations."""
import reflex as rx
from typing import List, Dict, Any
from datetime import datetime
from ..components.layout import layout
from ..auth import AuthState
from ..models_rafi import *

class CustomerDashboardState(rx.State):
    """Customer dashboard state management."""
    current_tab: str = "MENU"
    customer_id: str = ""
    
    # Data
    menu_items: List[Dict[str, Any]] = []
    meja_list: List[Dict[str, Any]] = []
    my_orders: List[Dict[str, Any]] = []
    
    # Order form
    selected_menu_id: str = ""
    selected_meja_id: str = ""
    is_order_dialog_open: bool = False
    order_success: str = ""
    order_error: str = ""
    
    def set_current_tab(self, tab: str):
        """Set current active tab."""
        self.current_tab = tab
        if tab == "MENU":
            self.load_menu_items()
        elif tab == "MEJA":
            self.load_meja_list()
        elif tab == "PESANAN":
            self.load_my_orders()
    
    def set_customer_id(self, customer_id: str):
        """Set customer ID from auth state."""
        self.customer_id = customer_id
        self.load_menu_items()
        self.load_meja_list()
        self.load_my_orders()
    
    async def load_menu_items(self):
        """Load available menu items."""
        try:
            with rx.session() as session:
                menus = session.query(Menu).all()
                self.menu_items = [
                    {
                        "ID_Menu": menu.ID_Menu,
                        "Nama_Menu": menu.Nama_Menu,
                        "Harga_Menu": menu.Harga_Menu,
                        "Kategori": menu.Kategori
                    }
                    for menu in menus
                ]
        except Exception as e:
            print(f"Error loading menu: {e}")
    
    async def load_meja_list(self):
        """Load available tables."""
        try:
            with rx.session() as session:
                meja = session.query(Meja).all()
                self.meja_list = [
                    {
                        "ID_Meja": m.ID_Meja,
                        "Nomor_Meja": m.Nomor_Meja,
                        "Status_Meja": m.Status_Meja
                    }
                    for m in meja
                ]
        except Exception as e:
            print(f"Error loading meja: {e}")
    
    async def load_my_orders(self):
        """Load customer's orders."""
        if not self.customer_id:
            return
            
        try:
            with rx.session() as session:
                orders = session.query(Pesanan).filter(
                    Pesanan.ID_Customer == self.customer_id
                ).all()
                
                self.my_orders = [
                    {
                        "ID_Pesanan": order.ID_Pesanan,
                        "ID_Customer": order.ID_Customer,
                        "Waktu_Pesanan": order.Waktu_Pesanan.strftime('%d-%m-%Y %H:%M'),
                        "ID_Menu": order.ID_Menu,
                        "ID_Meja": order.ID_Meja
                    }
                    for order in orders
                ]
        except Exception as e:
            print(f"Error loading orders: {e}")
    
    def open_order_dialog(self, menu_id: str):
        """Open order dialog for selected menu."""
        self.selected_menu_id = menu_id
        self.selected_meja_id = ""
        self.order_error = ""
        self.order_success = ""
        self.is_order_dialog_open = True
    
    def close_order_dialog(self):
        """Close order dialog."""
        self.is_order_dialog_open = False
        self.selected_menu_id = ""
        self.selected_meja_id = ""
        self.order_error = ""
        self.order_success = ""
    
    def set_selected_meja(self, meja_id: str):
        """Set selected meja for order."""
        self.selected_meja_id = meja_id
    
    async def submit_order(self):
        """Submit order to database."""
        if not self.selected_menu_id or not self.selected_meja_id:
            self.order_error = "Pilih menu dan meja terlebih dahulu!"
            return
        
        try:
            with rx.session() as session:
                # Generate new order ID
                new_id = generate_custom_id("PESANAN")
                
                # Create new order
                new_order = Pesanan(
                    ID_Pesanan=new_id,
                    ID_Customer=self.customer_id,
                    ID_Karyawan=None,
                    Waktu_Pesanan=datetime.now(),
                    ID_Menu=self.selected_menu_id,
                    ID_Meja=self.selected_meja_id
                )
                
                session.add(new_order)
                
                # Update table status
                meja = session.query(Meja).filter(Meja.ID_Meja == self.selected_meja_id).first()
                if meja:
                    meja.Status_Meja = "DIPESAN"
                
                session.commit()
                
                self.order_success = f"Pesanan berhasil dibuat dengan ID: {new_id}"
                self.order_error = ""
                
                # Refresh data
                await self.load_meja_list()
                await self.load_my_orders()
                
        except Exception as e:
            self.order_error = f"Gagal membuat pesanan: {str(e)}"
            self.order_success = ""

def menu_card(menu: Dict[str, Any]) -> rx.Component:
    """Create menu card component."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(menu["Nama_Menu"], class_name="text-white text-lg font-semibold"),
                    rx.text(menu["Kategori"], class_name="text-slate-400 text-sm"),
                    class_name="space-y-1 flex-1"
                ),
                rx.vstack(
                    rx.text(f"Rp {menu['Harga_Menu']:,.0f}", class_name="text-green-400 text-xl font-bold"),
                    rx.button(
                        "Pesan",
                        on_click=lambda: CustomerDashboardState.open_order_dialog(menu["ID_Menu"]),
                        class_name="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg",
                        size="2"
                    ),
                    class_name="space-y-2 items-end"
                ),
                class_name="flex justify-between items-start w-full"
            ),
            class_name="space-y-4"
        ),
        class_name="bg-slate-700/50 border border-slate-600 rounded-lg p-4 hover:bg-slate-700/70 transition-colors"
    )

def meja_card(meja: Dict[str, Any]) -> rx.Component:
    """Create meja card component."""
    status_colors = {
        "AVAILABLE": "bg-green-600",
        "DIPESAN": "bg-yellow-600", 
        "TERPAKAI": "bg-red-600"
    }
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(f"Meja {meja['Nomor_Meja']}", class_name="text-white text-lg font-semibold"),
                rx.box(
                    meja["Status_Meja"],
                    class_name=f"px-3 py-1 rounded-full text-white text-sm font-medium {status_colors.get(meja['Status_Meja'], 'bg-slate-600')}"
                ),
                class_name="flex justify-between items-center w-full"
            ),
            rx.text(f"ID: {meja['ID_Meja']}", class_name="text-slate-400 text-sm"),
            class_name="space-y-2"
        ),
        class_name="bg-slate-700/50 border border-slate-600 rounded-lg p-4"
    )

def order_card(order: Dict[str, Any]) -> rx.Component:
    """Create order card component."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(f"Order ID: {order['ID_Pesanan']}", class_name="text-white font-semibold"),
                rx.text(order["Waktu_Pesanan"], class_name="text-slate-400 text-sm"),
                class_name="flex justify-between items-center w-full"
            ),
            rx.hstack(
                rx.text(f"Menu: {order['ID_Menu']}", class_name="text-slate-300 text-sm"),
                rx.text(f"Meja: {order['ID_Meja']}", class_name="text-slate-300 text-sm"),
                class_name="flex justify-between w-full"
            ),
            class_name="space-y-2"
        ),
        class_name="bg-slate-700/50 border border-slate-600 rounded-lg p-4"
    )

def order_dialog() -> rx.Component:
    """Order dialog component."""
    available_meja = [meja for meja in CustomerDashboardState.meja_list if meja["Status_Meja"] == "AVAILABLE"]
    
    return rx.cond(
        CustomerDashboardState.is_order_dialog_open,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Pilih Meja", class_name="text-white text-xl font-semibold"),
                        rx.button(
                            rx.icon(tag="x", size=20),
                            on_click=CustomerDashboardState.close_order_dialog,
                            class_name="text-slate-400 hover:text-white bg-transparent border-none",
                            variant="ghost"
                        ),
                        class_name="flex justify-between items-center w-full"
                    ),
                    
                    rx.vstack(
                        rx.text("Pilih meja yang tersedia:", class_name="text-slate-300"),
                        rx.select(
                            [f"Meja {meja['Nomor_Meja']} ({meja['ID_Meja']})" for meja in available_meja],
                            value=CustomerDashboardState.selected_meja_id,
                            on_change=lambda value: CustomerDashboardState.set_selected_meja(
                                value.split("(")[1].split(")")[0] if "(" in value else value
                            ),
                            placeholder="Pilih meja...",
                            class_name="bg-slate-700 border-slate-600 text-white w-full"
                        ),
                        class_name="space-y-2 w-full"
                    ),
                    
                    # Success/Error messages
                    rx.cond(
                        CustomerDashboardState.order_success != "",
                        rx.box(
                            rx.hstack(
                                rx.icon(tag="check_circle", size=16, class_name="text-green-400"),
                                rx.text(CustomerDashboardState.order_success, class_name="text-green-400 text-sm"),
                                class_name="flex items-center space-x-2"
                            ),
                            class_name="p-3 bg-green-900/20 border border-green-500/30 rounded-lg"
                        )
                    ),
                    
                    rx.cond(
                        CustomerDashboardState.order_error != "",
                        rx.box(
                            rx.hstack(
                                rx.icon(tag="alert_circle", size=16, class_name="text-red-400"),
                                rx.text(CustomerDashboardState.order_error, class_name="text-red-400 text-sm"),
                                class_name="flex items-center space-x-2"
                            ),
                            class_name="p-3 bg-red-900/20 border border-red-500/30 rounded-lg"
                        )
                    ),
                    
                    rx.hstack(
                        rx.button(
                            "Batal",
                            on_click=CustomerDashboardState.close_order_dialog,
                            class_name="border-slate-600 text-slate-300 hover:bg-slate-700",
                            variant="outline"
                        ),
                        rx.button(
                            "Pesan",
                            on_click=CustomerDashboardState.submit_order,
                            class_name="bg-blue-600 hover:bg-blue-700 text-white"
                        ),
                        class_name="flex justify-end space-x-2 pt-4"
                    ),
                    
                    class_name="space-y-6"
                ),
                class_name="bg-slate-800 border-slate-700 text-white max-w-md w-full rounded-lg p-6"
            ),
            class_name="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        )
    )

def tab_button(tab_name: str, label: str, icon: str) -> rx.Component:
    """Create tab button."""
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon, size=16),
            rx.text(label),
            class_name="flex items-center space-x-2"
        ),
        on_click=lambda: CustomerDashboardState.set_current_tab(tab_name),
        class_name=f"""
            px-4 py-2 rounded-lg transition-all duration-200
            {
                'bg-blue-600 text-white shadow-lg' if CustomerDashboardState.current_tab == tab_name 
                else 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }
        """,
        variant="outline"
    )

def customer_dashboard_page() -> rx.Component:
    """Customer dashboard page."""
    
    # Set customer ID from auth state
    customer_id = AuthState.current_user.get("id", "") if AuthState.current_user else ""
    CustomerDashboardState.set_customer_id(customer_id)
    
    return layout(
        rx.vstack(
            # Header
            rx.vstack(
                rx.heading("Customer Dashboard", class_name="text-3xl font-bold text-white"),
                rx.text(f"Selamat datang, {customer_id}", class_name="text-slate-400"),
                class_name="text-center space-y-2"
            ),
            
            # Tab Navigation
            rx.box(
                rx.hstack(
                    tab_button("MENU", "Daftar Menu", "coffee"),
                    tab_button("MEJA", "Daftar Meja", "circle_dot"),
                    tab_button("PESANAN", "Pesanan Saya", "shopping_bag"),
                    class_name="flex space-x-2"
                ),
                class_name="bg-slate-800/50 border-slate-700 rounded-lg p-4"
            ),
            
            # Content based on current tab
            rx.cond(
                CustomerDashboardState.current_tab == "MENU",
                rx.box(
                    rx.vstack(
                        rx.heading("Daftar Menu", class_name="text-2xl font-bold text-white"),
                        rx.cond(
                            len(CustomerDashboardState.menu_items) > 0,
                            rx.grid(
                                *[menu_card(menu) for menu in CustomerDashboardState.menu_items],
                                columns="3",
                                spacing="4",
                                class_name="grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                            ),
                            rx.text("Tidak ada menu tersedia", class_name="text-slate-400 text-center py-8")
                        ),
                        class_name="space-y-4"
                    ),
                    class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
                )
            ),
            
            rx.cond(
                CustomerDashboardState.current_tab == "MEJA",
                rx.box(
                    rx.vstack(
                        rx.heading("Daftar Meja", class_name="text-2xl font-bold text-white"),
                        rx.cond(
                            len(CustomerDashboardState.meja_list) > 0,
                            rx.grid(
                                *[meja_card(meja) for meja in CustomerDashboardState.meja_list],
                                columns="4",
                                spacing="4",
                                class_name="grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
                            ),
                            rx.text("Tidak ada meja tersedia", class_name="text-slate-400 text-center py-8")
                        ),
                        class_name="space-y-4"
                    ),
                    class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
                )
            ),
            
            rx.cond(
                CustomerDashboardState.current_tab == "PESANAN",
                rx.box(
                    rx.vstack(
                        rx.heading("Pesanan Saya", class_name="text-2xl font-bold text-white"),
                        rx.cond(
                            len(CustomerDashboardState.my_orders) > 0,
                            rx.vstack(
                                *[order_card(order) for order in CustomerDashboardState.my_orders],
                                class_name="space-y-4"
                            ),
                            rx.text("Belum ada pesanan", class_name="text-slate-400 text-center py-8")
                        ),
                        class_name="space-y-4"
                    ),
                    class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
                )
            ),
            
            # Order Dialog
            order_dialog(),
            
            class_name="space-y-6"
        )
    )
