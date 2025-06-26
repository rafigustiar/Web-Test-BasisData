"""Main Amorty Cafe Management System application."""
import reflex as rx
from .auth import AuthState

# Simple landing page
def index() -> rx.Component:
    """Index page with welcome message."""
    return rx.container(
        rx.vstack(
            rx.heading("🎱 Amorty Cafe Management System", size="9"),
            rx.text("Sistem Manajemen Cafe Billiard Modern", size="5"),
            rx.button(
                "Masuk ke Aplikasi",
                on_click=rx.redirect("/login"),
                size="3",
                style={"margin_top": "20px"}
            ),
            spacing="4",
            align="center",
            justify="center",
            min_height="100vh"
        ),
        style={"text_align": "center"}
    )

# Simple login page with state
class LoginState(rx.State):
    admin_username: str = ""
    admin_password: str = ""
    customer_id: str = ""

    def handle_admin_login(self):
        return AuthState.login_admin(self.admin_username, self.admin_password)

    def handle_customer_login(self):
        return AuthState.login_customer(self.customer_id)

def login_page() -> rx.Component:
    """Login page."""
    return rx.container(
        rx.vstack(
            rx.heading("🔐 Login Amorty Cafe", size="8"),

            # Admin login section
            rx.card(
                rx.vstack(
                    rx.heading("👑 Admin Login", size="6"),
                    rx.input(
                        placeholder="Username Admin",
                        value=LoginState.admin_username,
                        on_change=LoginState.set_admin_username,
                        size="3"
                    ),
                    rx.input(
                        placeholder="Password Admin",
                        type="password",
                        value=LoginState.admin_password,
                        on_change=LoginState.set_admin_password,
                        size="3"
                    ),
                    rx.button(
                        "Login Admin",
                        on_click=LoginState.handle_admin_login,
                        size="3",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                width="300px"
            ),

            rx.text("atau", size="4", style={"margin": "20px 0"}),

            # Customer login section
            rx.card(
                rx.vstack(
                    rx.heading("👤 Customer Login", size="6"),
                    rx.input(
                        placeholder="Customer ID (contoh: CUS1)",
                        value=LoginState.customer_id,
                        on_change=LoginState.set_customer_id,
                        size="3"
                    ),
                    rx.button(
                        "Login Customer",
                        on_click=LoginState.handle_customer_login,
                        size="3",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                width="300px"
            ),

            # Error message
            rx.cond(
                AuthState.login_error != "",
                rx.text(
                    AuthState.login_error,
                    color="red",
                    size="3"
                )
            ),

            spacing="4",
            align="center",
            justify="center",
            min_height="100vh"
        ),
        style={"text_align": "center"}
    )

# Simple admin dashboard
def admin_dashboard() -> rx.Component:
    """Admin dashboard."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("👑 Admin Dashboard - Amorty Cafe", size="8"),
                rx.button(
                    "Logout",
                    on_click=AuthState.logout,
                    size="3"
                ),
                justify="between",
                width="100%"
            ),

            rx.text("Selamat datang di sistem manajemen Amorty Cafe!", size="5"),
            rx.text("Dashboard admin akan dikembangkan lebih lanjut.", size="4"),

            # Simple stats cards
            rx.hstack(
                rx.card("📊 Total Customer: 0"),
                rx.card("🎱 Total Meja: 0"),
                rx.card("🍽️ Total Menu: 0"),
                rx.card("💰 Total Transaksi: 0"),
                spacing="4"
            ),

            spacing="6",
            width="100%",
            padding="20px"
        )
    )

# Simple customer dashboard
def customer_dashboard() -> rx.Component:
    """Customer dashboard."""
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading("👤 Customer Dashboard - Amorty Cafe", size="8"),
                rx.button(
                    "Logout",
                    on_click=AuthState.logout,
                    size="3"
                ),
                justify="between",
                width="100%"
            ),

            rx.text(f"Selamat datang, Customer {AuthState.current_user.get('customer_id', '')}!", size="5"),
            rx.text("Dashboard customer akan dikembangkan lebih lanjut.", size="4"),

            # Simple menu
            rx.hstack(
                rx.card("🍽️ Lihat Menu"),
                rx.card("🎱 Status Meja"),
                rx.card("📋 Riwayat Pesanan"),
                spacing="4"
            ),

            spacing="6",
            width="100%",
            padding="20px"
        )
    )

# Create the main app
app = rx.App()

# Add pages
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(admin_dashboard, route="/admin-dashboard")
app.add_page(customer_dashboard, route="/customer-dashboard")
