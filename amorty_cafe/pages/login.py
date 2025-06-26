"""Login page for Amorty Cafe Management System."""
import reflex as rx
from ..auth import AuthState

class LoginFormState(rx.State):
    """Login form state."""
    username: str = ""
    password: str = ""
    role: str = "customer"  # customer or admin
    
    def set_username(self, value: str):
        self.username = value
    
    def set_password(self, value: str):
        self.password = value
    
    def set_role(self, value: str):
        self.role = value
    
    async def handle_login(self):
        """Handle login form submission."""
        if self.username and self.password:
            await AuthState.login(self.username, self.password)

def login_page() -> rx.Component:
    """Login page component."""
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
                            "Sign In",
                            class_name="text-2xl font-bold text-white text-center mb-6"
                        ),
                        
                        # Role Selection
                        rx.vstack(
                            rx.text("Login as:", class_name="text-sm font-medium text-slate-300"),
                            rx.hstack(
                                rx.button(
                                    "Customer",
                                    on_click=lambda: LoginFormState.set_role("customer"),
                                    class_name=f"""
                                        px-4 py-2 rounded-lg transition-all duration-200
                                        {'bg-blue-600 text-white' if LoginFormState.role == 'customer' else 'bg-slate-700 text-slate-300 hover:bg-slate-600'}
                                    """,
                                    variant="outline"
                                ),
                                rx.button(
                                    "Admin",
                                    on_click=lambda: LoginFormState.set_role("admin"),
                                    class_name=f"""
                                        px-4 py-2 rounded-lg transition-all duration-200
                                        {'bg-blue-600 text-white' if LoginFormState.role == 'admin' else 'bg-slate-700 text-slate-300 hover:bg-slate-600'}
                                    """,
                                    variant="outline"
                                ),
                                class_name="flex space-x-2"
                            ),
                            class_name="space-y-2"
                        ),
                        
                        # Username Field
                        rx.vstack(
                            rx.text("Username", class_name="text-sm font-medium text-slate-300"),
                            rx.input(
                                placeholder="Enter your username",
                                value=LoginFormState.username,
                                on_change=LoginFormState.set_username,
                                class_name="""
                                    bg-slate-700/50 border-slate-600 text-white placeholder-slate-400
                                    focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                                """,
                                type="text"
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Password Field
                        rx.vstack(
                            rx.text("Password", class_name="text-sm font-medium text-slate-300"),
                            rx.input(
                                placeholder="Enter your password",
                                value=LoginFormState.password,
                                on_change=LoginFormState.set_password,
                                class_name="""
                                    bg-slate-700/50 border-slate-600 text-white placeholder-slate-400
                                    focus:border-blue-500 focus:ring-1 focus:ring-blue-500
                                """,
                                type="password"
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Error Message
                        rx.cond(
                            AuthState.login_error != "",
                            rx.text(
                                AuthState.login_error,
                                class_name="text-red-400 text-sm text-center"
                            )
                        ),
                        
                        # Login Button
                        rx.button(
                            "Sign In",
                            on_click=LoginFormState.handle_login,
                            class_name="""
                                w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800
                                text-white font-medium py-3 rounded-lg transition-all duration-200
                                shadow-lg hover:shadow-blue-600/25
                            """,
                            size="3"
                        ),
                        
                        # Sign Up Link
                        rx.hstack(
                            rx.text("Don't have an account?", class_name="text-sm text-slate-400"),
                            rx.link(
                                "Sign up",
                                href="/signup",
                                class_name="text-sm text-blue-400 hover:text-blue-300 font-medium"
                            ),
                            class_name="justify-center"
                        ),
                        
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
        
        # Background
        rx.box(
            rx.box(class_name="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"),
            rx.box(
                class_name="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse",
                style={"animation_delay": "1s"}
            ),
            class_name="fixed inset-0 -z-10 overflow-hidden pointer-events-none"
        ),
        
        class_name="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
    )
