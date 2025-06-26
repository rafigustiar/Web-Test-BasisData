"""Simple working Amorty Cafe app."""
import reflex as rx

class AppState(rx.State):
    """Simple app state."""
    is_logged_in: bool = False
    current_page: str = "login"
    username: str = ""
    password: str = ""
    customer_id: str = ""
    error_message: str = ""
    
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

def login_page():
    """Login page component."""
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
                        value=AppState.username,
                        on_change=AppState.set_username,
                    ),
                    rx.input(
                        placeholder="Password",
                        type="password",
                        value=AppState.password,
                        on_change=AppState.set_password,
                    ),
                    rx.button(
                        "Login Admin",
                        on_click=AppState.admin_login,
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
                        value=AppState.customer_id,
                        on_change=AppState.set_customer_id,
                    ),
                    rx.button(
                        "Login Customer",
                        on_click=AppState.customer_login,
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
                AppState.error_message != "",
                rx.text(AppState.error_message, color="red"),
            ),
            
            spacing="4",
            align="center",
        ),
        height="100vh",
    )

def admin_page():
    """Admin dashboard component."""
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("👑 Admin Dashboard - Amorty Cafe", size="8"),
                rx.button("Logout", on_click=AppState.logout),
                justify="between",
                width="100%",
            ),
            rx.text("Selamat datang di admin dashboard!", size="5"),
            rx.text("Dashboard lengkap akan dikembangkan selanjutnya.", size="4"),
            
            # Simple cards
            rx.hstack(
                rx.box("📊 Total Customer: 0", p="4", bg="blue.100"),
                rx.box("🎱 Total Meja: 0", p="4", bg="green.100"),
                rx.box("🍽️ Total Menu: 0", p="4", bg="yellow.100"),
                rx.box("💰 Total Transaksi: 0", p="4", bg="red.100"),
                spacing="4",
            ),
            
            spacing="6",
            p="6",
        )
    )

def customer_page():
    """Customer dashboard component."""
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("👤 Customer Dashboard - Amorty Cafe", size="8"),
                rx.button("Logout", on_click=AppState.logout),
                justify="between",
                width="100%",
            ),
            rx.text(f"Selamat datang, Customer {AppState.customer_id}!", size="5"),
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
        AppState.is_logged_in,
        rx.cond(
            AppState.current_page == "admin",
            admin_page(),
            customer_page(),
        ),
        login_page(),
    )

# Create app
app = rx.App()
app.add_page(index, route="/")
