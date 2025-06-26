"""Enhanced login page with admin/customer role selection."""
import reflex as rx
from ..auth import AuthState
from ..models_rafi import Customer

class LoginFormState(rx.State):
    """Enhanced login form state with role selection."""
    username: str = ""
    password: str = ""
    role: str = "Customer"  # Customer or Admin
    login_error: str = ""
    is_loading: bool = False
    
    def set_username(self, value: str):
        self.username = value
        self.login_error = ""
    
    def set_password(self, value: str):
        self.password = value
        self.login_error = ""
    
    def set_role(self, value: str):
        self.role = value
        self.login_error = ""
        # Clear password field when switching to customer
        if value == "Customer":
            self.password = ""
    
    async def handle_login(self):
        """Handle login with role-based authentication."""
        self.is_loading = True
        self.login_error = ""
        
        if not self.username:
            self.login_error = "Username/ID Customer harus diisi"
            self.is_loading = False
            return
        
        try:
            if self.role == "Admin":
                # Admin login with hardcoded credentials
                if self.username == "admin" and self.password == "admin":
                    AuthState.current_user = {
                        "id": "admin",
                        "username": "admin",
                        "role": "admin",
                        "name": "Administrator"
                    }
                    AuthState.is_authenticated = True
                    self.is_loading = False
                    return rx.redirect("/admin-dashboard")
                else:
                    self.login_error = "Username atau password admin salah"
            else:
                # Customer login - verify ID exists in database
                if await self.verify_customer(self.username):
                    AuthState.current_user = {
                        "id": self.username,
                        "username": self.username,
                        "role": "customer",
                        "name": f"Customer {self.username}"
                    }
                    AuthState.is_authenticated = True
                    self.is_loading = False
                    return rx.redirect("/customer-dashboard")
                else:
                    self.login_error = "ID Customer tidak ditemukan"
        
        except Exception as e:
            self.login_error = f"Error saat login: {str(e)}"
        
        self.is_loading = False
    
    async def verify_customer(self, customer_id: str) -> bool:
        """Verify customer ID exists in database."""
        try:
            with rx.session() as session:
                customer = session.query(Customer).filter(Customer.ID_Customer == customer_id).first()
                return customer is not None
        except Exception as e:
            print(f"Error verifying customer: {e}")
            return False

def role_selector() -> rx.Component:
    """Role selection component."""
    return rx.vstack(
        rx.text("Pilih Peran:", class_name="text-sm font-medium text-slate-300"),
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon(tag="user", size=16),
                    rx.text("Customer"),
                    class_name="flex items-center space-x-2"
                ),
                on_click=lambda: LoginFormState.set_role("Customer"),
                class_name=f"""
                    px-4 py-3 rounded-lg transition-all duration-200 flex-1
                    {'bg-blue-600 text-white shadow-lg' if LoginFormState.role == 'Customer' 
                     else 'bg-slate-700 text-slate-300 hover:bg-slate-600 border border-slate-600'}
                """,
                variant="outline"
            ),
            rx.button(
                rx.hstack(
                    rx.icon(tag="shield", size=16),
                    rx.text("Admin"),
                    class_name="flex items-center space-x-2"
                ),
                on_click=lambda: LoginFormState.set_role("Admin"),
                class_name=f"""
                    px-4 py-3 rounded-lg transition-all duration-200 flex-1
                    {'bg-blue-600 text-white shadow-lg' if LoginFormState.role == 'Admin' 
                     else 'bg-slate-700 text-slate-300 hover:bg-slate-600 border border-slate-600'}
                """,
                variant="outline"
            ),
            class_name="flex space-x-3 w-full"
        ),
        class_name="space-y-3"
    )

def login_form() -> rx.Component:
    """Enhanced login form."""
    return rx.vstack(
        # Role Selection
        role_selector(),
        
        # Username/ID Field
        rx.vstack(
            rx.text(
                rx.cond(
                    LoginFormState.role == "Admin",
                    "Username",
                    "ID Customer"
                ),
                class_name="text-sm font-medium text-slate-300"
            ),
            rx.input(
                placeholder=rx.cond(
                    LoginFormState.role == "Admin",
                    "Masukkan username admin",
                    "Masukkan ID Customer (contoh: CUS1)"
                ),
                value=LoginFormState.username,
                on_change=LoginFormState.set_username,
                class_name="""
                    bg-slate-700/50 border-slate-600 text-white placeholder-slate-400
                    focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                """,
                type="text"
            ),
            class_name="space-y-2"
        ),
        
        # Password Field (only for Admin)
        rx.cond(
            LoginFormState.role == "Admin",
            rx.vstack(
                rx.text("Password", class_name="text-sm font-medium text-slate-300"),
                rx.input(
                    placeholder="Masukkan password admin",
                    value=LoginFormState.password,
                    on_change=LoginFormState.set_password,
                    class_name="""
                        bg-slate-700/50 border-slate-600 text-white placeholder-slate-400
                        focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                    """,
                    type="password"
                ),
                class_name="space-y-2"
            )
        ),
        
        # Error Message
        rx.cond(
            LoginFormState.login_error != "",
            rx.box(
                rx.hstack(
                    rx.icon(tag="alert_circle", size=16, class_name="text-red-400"),
                    rx.text(
                        LoginFormState.login_error,
                        class_name="text-red-400 text-sm"
                    ),
                    class_name="flex items-center space-x-2"
                ),
                class_name="p-3 bg-red-900/20 border border-red-500/30 rounded-lg"
            )
        ),
        
        # Login Button
        rx.button(
            rx.cond(
                LoginFormState.is_loading,
                rx.hstack(
                    rx.spinner(size="4"),
                    rx.text("Masuk..."),
                    class_name="flex items-center space-x-2"
                ),
                rx.hstack(
                    rx.icon(tag="log_in", size=16),
                    rx.text("Masuk"),
                    class_name="flex items-center space-x-2"
                )
            ),
            on_click=LoginFormState.handle_login,
            disabled=LoginFormState.is_loading,
            class_name="""
                w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800
                text-white font-medium py-3 rounded-lg transition-all duration-200
                shadow-lg hover:shadow-blue-600/25 disabled:opacity-50 disabled:cursor-not-allowed
            """,
            size="3"
        ),
        
        # Info Box
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon(tag="info", size=16, class_name="text-blue-400"),
                    rx.text("Info Login", class_name="font-medium text-blue-400"),
                    class_name="flex items-center space-x-2"
                ),
                rx.vstack(
                    rx.text("• Admin: username=admin, password=admin", class_name="text-xs text-slate-400"),
                    rx.text("• Customer: gunakan ID Customer dari database", class_name="text-xs text-slate-400"),
                    rx.text("• Contoh ID Customer: CUS1, CUS2, dst.", class_name="text-xs text-slate-400"),
                    class_name="space-y-1"
                ),
                class_name="space-y-2"
            ),
            class_name="p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg"
        ),
        
        class_name="space-y-4 w-full"
    )

def login_page() -> rx.Component:
    """Enhanced login page component."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Logo Section
                rx.vstack(
                    rx.box(
                        rx.box(
                            class_name="""
                                w-20 h-20 rounded-2xl shadow-2xl bg-no-repeat bg-center bg-cover mx-auto
                            """,
                            style={
                                "background_image": "url(https://cdn.builder.io/api/v1/image/assets%2F420a2dccf542446cabbce903b3e093cd%2F595bdb5ec74c409aba04ec2433147a93)"
                            }
                        ),
                        rx.box(
                            class_name="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full border-4 border-slate-900"
                        ),
                        class_name="relative"
                    ),
                    rx.heading(
                        "Amorty",
                        class_name="text-4xl font-bold text-white tracking-tight"
                    ),
                    rx.text(
                        "BILLIARDS & CAFE",
                        class_name="text-sm text-slate-400 font-medium tracking-wider"
                    ),
                    rx.text(
                        "Management System",
                        class_name="text-lg text-slate-300 font-medium"
                    ),
                    class_name="text-center space-y-2",
                    spacing="2"
                ),
                
                # Login Form
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Selamat Datang",
                            class_name="text-2xl font-bold text-white text-center mb-2"
                        ),
                        rx.text(
                            "Silakan masuk ke sistem manajemen cafe",
                            class_name="text-slate-400 text-center mb-6"
                        ),
                        
                        login_form(),
                        
                        class_name="space-y-4"
                    ),
                    class_name="""
                        bg-slate-800/60 backdrop-blur-lg border border-slate-700/50 rounded-2xl p-8
                        shadow-2xl w-full max-w-md
                    """
                ),
                
                class_name="min-h-screen flex flex-col justify-center items-center space-y-8"
            ),
            class_name="max-w-md mx-auto px-4"
        ),
        
        # Background Elements
        rx.box(
            rx.box(class_name="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/8 rounded-full blur-3xl animate-pulse"),
            rx.box(
                class_name="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/8 rounded-full blur-3xl animate-pulse",
                style={"animation_delay": "1s"}
            ),
            rx.box(
                class_name="absolute top-1/2 left-1/2 w-96 h-96 bg-green-500/5 rounded-full blur-3xl animate-pulse transform -translate-x-1/2 -translate-y-1/2",
                style={"animation_delay": "2s"}
            ),
            class_name="fixed inset-0 -z-10 overflow-hidden pointer-events-none"
        ),
        
        class_name="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
    )
