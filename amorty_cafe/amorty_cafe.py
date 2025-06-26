"""Main Amorty Cafe Management System application."""
import reflex as rx
from .pages.login_rafi import login_page
from .pages.admin_dashboard import admin_dashboard_page
from .pages.customer_dashboard import customer_dashboard_page
from .auth import AuthState

# Add routes
def index() -> rx.Component:
    """Index page redirects based on authentication and role."""
    return rx.cond(
        AuthState.is_authenticated,
        rx.cond(
            AuthState.current_user.get("role") == "admin",
            rx.redirect("/admin-dashboard"),
            rx.redirect("/customer-dashboard")
        ),
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
app.add_page(admin_dashboard_page, route="/admin-dashboard")
app.add_page(customer_dashboard_page, route="/customer-dashboard")

if __name__ == "__main__":
    app.run()
