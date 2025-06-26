"""Main Amorty Cafe Management System application."""
import reflex as rx
from .pages.login import login_page
from .pages.signup import signup_page
from .pages.dashboard import dashboard_page
from .auth import AuthState

# Add routes
def index() -> rx.Component:
    """Index page redirects to dashboard or login."""
    return rx.cond(
        AuthState.is_authenticated,
        dashboard_page(),
        rx.redirect("/login")
    )

# Create the main app
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        gray_color="slate",
        radius="medium",
        scaling="100%"
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ]
)

# Add pages
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(dashboard_page, route="/dashboard")

# Add customer dashboard (simplified version)
@rx.page(route="/customer-dashboard")
def customer_dashboard():
    """Customer dashboard page."""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading("Customer Dashboard", class_name="text-3xl font-bold text-white text-center"),
                rx.text("Welcome to Amorty Billiards & Cafe!", class_name="text-xl text-slate-400 text-center"),
                rx.button(
                    "Logout",
                    on_click=AuthState.logout,
                    class_name="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg"
                ),
                class_name="min-h-screen flex flex-col justify-center items-center space-y-8"
            ),
            class_name="max-w-4xl mx-auto px-4"
        ),
        class_name="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
    )

if __name__ == "__main__":
    app.run()
