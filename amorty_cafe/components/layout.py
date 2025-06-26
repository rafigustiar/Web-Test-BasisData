"""Main layout component for Amorty Cafe Management System."""
import reflex as rx
from typing import List, Dict, Any
from ..auth import AuthState

def navigation_item(href: str, label: str, icon_name: str, is_active: bool = False) -> rx.Component:
    """Create a navigation item."""
    return rx.link(
        rx.hstack(
            rx.icon(
                tag=icon_name,
                size=16,
                class_name=f"transition-transform duration-200 {'scale-110' if is_active else 'group-hover:scale-105'}"
            ),
            rx.text(
                label,
                class_name="hidden xl:inline text-sm font-medium"
            ),
            class_name=f"""
                relative flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium 
                transition-all duration-200 group
                {
                    'bg-blue-600/90 text-white shadow-lg shadow-blue-600/25' if is_active 
                    else 'text-slate-300 hover:text-white hover:bg-slate-700/60'
                }
            """
        ),
        href=href,
        class_name="block"
    )

def mobile_nav_item(href: str, label: str, icon_name: str, is_active: bool = False) -> rx.Component:
    """Create a mobile navigation item."""
    return rx.link(
        rx.hstack(
            rx.icon(tag=icon_name, size=16),
            rx.text(label),
            class_name=f"""
                flex items-center space-x-3 px-3 py-3 rounded-lg text-sm font-medium 
                transition-all duration-200
                {
                    'bg-blue-600/90 text-white shadow-lg' if is_active 
                    else 'text-slate-300 hover:text-white hover:bg-slate-700/60'
                }
            """
        ),
        href=href
    )

class LayoutState(rx.State):
    """Layout state management."""
    is_mobile_menu_open: bool = False
    current_path: str = "/"
    
    def toggle_mobile_menu(self):
        """Toggle mobile menu."""
        self.is_mobile_menu_open = not self.is_mobile_menu_open
    
    def close_mobile_menu(self):
        """Close mobile menu."""
        self.is_mobile_menu_open = False
    
    def set_current_path(self, path: str):
        """Set current path for navigation highlighting."""
        self.current_path = path

def header() -> rx.Component:
    """Create the header component."""
    return rx.box(
        rx.container(
            rx.hstack(
                # Logo Section
                rx.hstack(
                    rx.box(
                        rx.box(
                            class_name="""
                                w-10 h-10 rounded-xl shadow-lg bg-no-repeat bg-center bg-cover
                            """,
                            style={
                                "background_image": "url(https://cdn.builder.io/api/v1/image/assets%2F420a2dccf542446cabbce903b3e093cd%2F595bdb5ec74c409aba04ec2433147a93)"
                            }
                        ),
                        rx.box(
                            class_name="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900"
                        ),
                        class_name="relative"
                    ),
                    rx.vstack(
                        rx.heading(
                            "Amorty",
                            class_name="text-xl font-bold text-white tracking-tight"
                        ),
                        rx.text(
                            "BILLIARDS & CAFE",
                            class_name="text-xs text-slate-400 font-medium tracking-wider"
                        ),
                        class_name="flex flex-col",
                        spacing="0"
                    ),
                    class_name="flex items-center space-x-3"
                ),
                
                # Desktop Navigation
                rx.hstack(
                    navigation_item("/", "Dashboard", "layout_dashboard", LayoutState.current_path == "/"),
                    navigation_item("/customers", "Customers", "users", LayoutState.current_path == "/customers"),
                    navigation_item("/employees", "Staff", "user_check", LayoutState.current_path == "/employees"),
                    navigation_item("/menu", "Menu", "coffee", LayoutState.current_path == "/menu"),
                    navigation_item("/orders", "Orders", "shopping_cart", LayoutState.current_path == "/orders"),
                    navigation_item("/payments", "Payments", "credit_card", LayoutState.current_path == "/payments"),
                    navigation_item("/reservations", "Reservations", "calendar", LayoutState.current_path == "/reservations"),
                    navigation_item("/rentals", "Rentals", "receipt", LayoutState.current_path == "/rentals"),
                    navigation_item("/tables", "Tables", "circle_dot", LayoutState.current_path == "/tables"),
                    class_name="hidden lg:flex items-center space-x-1"
                ),
                
                # Right Side Actions
                rx.hstack(
                    # Notifications
                    rx.button(
                        rx.icon(tag="bell", size=16),
                        rx.box(
                            class_name="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"
                        ),
                        class_name="relative text-slate-400 hover:text-white hover:bg-slate-700/50",
                        variant="ghost",
                        size="2"
                    ),
                    
                    # Settings
                    rx.button(
                        rx.icon(tag="settings", size=16),
                        class_name="text-slate-400 hover:text-white hover:bg-slate-700/50",
                        variant="ghost",
                        size="2"
                    ),
                    
                    # Divider
                    rx.box(class_name="w-px h-6 bg-slate-600"),
                    
                    # Phone
                    rx.hstack(
                        rx.text("Tel:", class_name="text-xs text-slate-400"),
                        rx.text("(0341) 487789", class_name="text-xs text-slate-300"),
                        class_name="flex items-center space-x-2"
                    ),
                    
                    # Staff Area / Logout
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.button(
                            f"Logout ({AuthState.current_user['username'] if AuthState.current_user else ''})",
                            on_click=AuthState.logout,
                            class_name="""
                                bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 
                                text-white shadow-lg hover:shadow-red-600/25 transition-all duration-200
                            """,
                            size="2"
                        ),
                        rx.button(
                            "Staff Area",
                            class_name="""
                                bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-700 hover:to-pink-800 
                                text-white shadow-lg hover:shadow-pink-600/25 transition-all duration-200
                            """,
                            size="2"
                        )
                    ),
                    
                    class_name="hidden lg:flex items-center space-x-3"
                ),
                
                # Mobile Menu Button
                rx.button(
                    rx.cond(
                        LayoutState.is_mobile_menu_open,
                        rx.icon(tag="x", size=20),
                        rx.icon(tag="menu", size=20)
                    ),
                    on_click=LayoutState.toggle_mobile_menu,
                    class_name="lg:hidden text-white hover:bg-slate-700/50",
                    variant="ghost",
                    size="2"
                ),
                
                class_name="flex justify-between items-center h-16"
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        ),
        class_name="sticky top-0 z-50 bg-black/30 backdrop-blur-lg border-b border-slate-700/50"
    )

def mobile_menu() -> rx.Component:
    """Create mobile menu."""
    return rx.cond(
        LayoutState.is_mobile_menu_open,
        rx.box(
            rx.container(
                rx.vstack(
                    rx.grid(
                        mobile_nav_item("/", "Dashboard", "layout_dashboard", LayoutState.current_path == "/"),
                        mobile_nav_item("/customers", "Customers", "users", LayoutState.current_path == "/customers"),
                        mobile_nav_item("/employees", "Staff", "user_check", LayoutState.current_path == "/employees"),
                        mobile_nav_item("/menu", "Menu", "coffee", LayoutState.current_path == "/menu"),
                        mobile_nav_item("/orders", "Orders", "shopping_cart", LayoutState.current_path == "/orders"),
                        mobile_nav_item("/payments", "Payments", "credit_card", LayoutState.current_path == "/payments"),
                        mobile_nav_item("/reservations", "Reservations", "calendar", LayoutState.current_path == "/reservations"),
                        mobile_nav_item("/rentals", "Rentals", "receipt", LayoutState.current_path == "/rentals"),
                        mobile_nav_item("/tables", "Tables", "circle_dot", LayoutState.current_path == "/tables"),
                        columns="2",
                        spacing="2",
                        class_name="grid-cols-2 gap-2 mb-4"
                    ),
                    
                    # Mobile Actions
                    rx.vstack(
                        rx.hstack(
                            rx.text("Tel: (0341) 487789", class_name="text-xs text-slate-400"),
                            rx.hstack(
                                rx.button(
                                    rx.icon(tag="bell", size=16),
                                    class_name="text-slate-400 hover:text-white",
                                    variant="ghost",
                                    size="2"
                                ),
                                rx.button(
                                    rx.icon(tag="settings", size=16),
                                    class_name="text-slate-400 hover:text-white",
                                    variant="ghost",
                                    size="2"
                                ),
                                class_name="flex items-center space-x-2"
                            ),
                            class_name="flex items-center justify-between"
                        ),
                        rx.cond(
                            AuthState.is_authenticated,
                            rx.button(
                                f"Logout ({AuthState.current_user['username'] if AuthState.current_user else ''})",
                                on_click=AuthState.logout,
                                class_name="""
                                    w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 
                                    text-white
                                """,
                                size="2"
                            ),
                            rx.button(
                                "Staff Area",
                                class_name="""
                                    w-full bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-700 hover:to-pink-800 
                                    text-white
                                """,
                                size="2"
                            )
                        ),
                        class_name="pt-4 border-t border-slate-700/50 space-y-3"
                    ),
                    
                    class_name="py-4"
                ),
                class_name="max-w-7xl mx-auto px-4"
            ),
            class_name="lg:hidden bg-black/40 backdrop-blur-lg border-b border-slate-700/50"
        )
    )

def layout(children: rx.Component) -> rx.Component:
    """Main layout wrapper."""
    return rx.box(
        header(),
        mobile_menu(),
        rx.container(
            children,
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
        ),
        # Background elements
        rx.box(
            rx.box(class_name="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/3 rounded-full blur-3xl animate-pulse"),
            rx.box(
                class_name="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/3 rounded-full blur-3xl animate-pulse",
                style={"animation_delay": "1s"}
            ),
            rx.box(
                class_name="""
                    absolute top-1/2 left-1/2 w-96 h-96 bg-green-500/2 rounded-full blur-3xl 
                    transform -translate-x-1/2 -translate-y-1/2 animate-pulse
                """,
                style={"animation_delay": "2s"}
            ),
            class_name="fixed inset-0 -z-10 overflow-hidden pointer-events-none"
        ),
        class_name="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
    )
