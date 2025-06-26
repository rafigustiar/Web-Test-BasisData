"""Dashboard page for Amorty Cafe Management System."""
import reflex as rx
from typing import List, Dict, Any
from ..components.layout import layout, LayoutState
from ..auth import AuthState, require_auth
from ..models import *

class DashboardState(rx.State):
    """Dashboard state management."""
    total_customers: int = 0
    total_employees: int = 0
    total_menu_items: int = 0
    total_tables: int = 0
    today_orders: int = 0
    today_revenue: float = 0.0
    active_rentals: int = 0
    pending_reservations: int = 0
    available_tables: int = 0
    
    recent_orders: List[Dict[str, Any]] = []
    upcoming_reservations: List[Dict[str, Any]] = []
    active_rental_list: List[Dict[str, Any]] = []
    
    async def load_dashboard_data(self):
        """Load dashboard statistics and data."""
        with rx.session() as session:
            # Get statistics
            self.total_customers = session.query(Customer).count()
            self.total_employees = session.query(Employee).count()
            self.total_menu_items = session.query(MenuCafe).count()
            self.total_tables = session.query(BilliardTable).count()
            
            # Today's orders and revenue
            from datetime import datetime, date
            today = date.today()
            today_orders = session.query(Order).filter(
                rx.text.cast(Order.order_date, rx.Date) == today
            ).all()
            
            self.today_orders = len(today_orders)
            self.today_revenue = sum(order.total_amount for order in today_orders)
            
            # Active rentals
            self.active_rentals = session.query(RentalTransaction).filter(
                RentalTransaction.status == RentalStatus.ACTIVE
            ).count()
            
            # Pending reservations
            self.pending_reservations = session.query(Reservation).filter(
                Reservation.status == ReservationStatus.PENDING
            ).count()
            
            # Available tables
            self.available_tables = session.query(BilliardTable).filter(
                BilliardTable.status == TableStatus.AVAILABLE
            ).count()
            
            # Recent orders (last 5)
            recent_orders = session.query(Order).order_by(Order.order_date.desc()).limit(5).all()
            self.recent_orders = [
                {
                    "id": order.id,
                    "customer_name": order.customer_name,
                    "total_amount": order.total_amount,
                    "status": order.status.value,
                    "order_date": order.order_date.strftime("%H:%M")
                }
                for order in recent_orders
            ]
            
            # Upcoming reservations (next 3)
            upcoming_reservations = session.query(Reservation).filter(
                Reservation.reservation_date >= today
            ).order_by(Reservation.reservation_date.asc()).limit(3).all()
            
            self.upcoming_reservations = [
                {
                    "id": res.id,
                    "customer_name": res.customer_name,
                    "table_number": res.table_number,
                    "start_time": res.start_time,
                    "end_time": res.end_time,
                    "status": res.status.value
                }
                for res in upcoming_reservations
            ]
            
            # Active rentals
            active_rentals = session.query(RentalTransaction).filter(
                RentalTransaction.status == RentalStatus.ACTIVE
            ).all()
            
            self.active_rental_list = [
                {
                    "id": rental.id,
                    "customer_name": rental.customer_name,
                    "table_number": rental.table_number,
                    "duration": rental.duration,
                    "total_amount": rental.total_amount,
                    "start_time": rental.start_time.strftime("%H:%M")
                }
                for rental in active_rentals
            ]

def metric_card(title: str, value: str, subtitle: str, icon_name: str, gradient_class: str) -> rx.Component:
    """Create a metric card component."""
    return rx.box(
        rx.box(
            class_name=f"absolute inset-0 {gradient_class}"
        ),
        rx.hstack(
            rx.vstack(
                rx.text(title, class_name="text-sm font-medium text-white"),
                rx.text(value, class_name="text-3xl font-bold text-white"),
                rx.hstack(
                    rx.icon(tag="trending_up", size=12),
                    rx.text(subtitle, class_name="text-xs text-white/80"),
                    class_name="flex items-center mt-1"
                ),
                class_name="space-y-0",
                spacing="1"
            ),
            rx.box(
                rx.icon(
                    tag=icon_name,
                    size=16,
                    class_name="transition-colors group-hover:scale-105"
                ),
                class_name=f"""
                    p-2 bg-white/10 rounded-lg group-hover:bg-white/20 transition-colors 
                    border border-white/10
                """
            ),
            class_name="flex justify-between items-start space-y-0 pb-2 relative z-10"
        ),
        class_name="""
            relative overflow-hidden bg-slate-800/60 border-slate-700/50 hover:border-slate-600/70 
            transition-all duration-300 group backdrop-blur-sm rounded-lg p-6
        """
    )

def secondary_card(title: str, value: str, subtitle: str, icon_name: str) -> rx.Component:
    """Create a secondary metric card."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(title, class_name="text-sm font-medium text-slate-200"),
                rx.text(value, class_name="text-2xl font-bold text-white"),
                rx.text(subtitle, class_name="text-xs text-slate-400"),
                class_name="space-y-0",
                spacing="1"
            ),
            rx.icon(tag=icon_name, size=16, class_name="text-slate-400"),
            class_name="flex justify-between items-start space-y-0 pb-2"
        ),
        class_name="""
            bg-slate-800/40 border-slate-700/50 hover:bg-slate-800/60 transition-colors 
            backdrop-blur-sm rounded-lg p-6
        """
    )

def activity_card(title: str, icon_name: str, items: List[Dict[str, Any]], item_renderer) -> rx.Component:
    """Create an activity card component."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag=icon_name, size=20),
                rx.heading(title, class_name="text-white"),
                class_name="flex items-center"
            ),
            rx.vstack(
                *[item_renderer(item) for item in items],
                class_name="space-y-4"
            ) if items else rx.text("No recent activity", class_name="text-slate-400 text-center py-8"),
            class_name="space-y-4"
        ),
        class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
    )

def order_item(order: Dict[str, Any]) -> rx.Component:
    """Render an order item."""
    status_colors = {
        "Served": "bg-green-600",
        "Preparing": "bg-blue-600",
        "Ready": "bg-yellow-600",
        "Pending": "bg-orange-600",
        "Cancelled": "bg-red-600"
    }
    
    return rx.hstack(
        rx.vstack(
            rx.text(order["customer_name"], class_name="font-medium text-white"),
            rx.text(
                f"${order['total_amount']:.2f} • {order['order_date']}",
                class_name="text-sm text-slate-400"
            ),
            class_name="space-y-0",
            spacing="0"
        ),
        rx.box(
            order["status"],
            class_name=f"""
                px-2 py-1 rounded text-xs font-medium text-white
                {status_colors.get(order['status'], 'bg-slate-600')}
            """
        ),
        class_name="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg"
    )

def reservation_item(reservation: Dict[str, Any]) -> rx.Component:
    """Render a reservation item."""
    status_colors = {
        "Confirmed": "bg-green-600",
        "Pending": "bg-yellow-600",
        "Cancelled": "bg-red-600"
    }
    
    return rx.hstack(
        rx.vstack(
            rx.text(reservation["customer_name"], class_name="font-medium text-white"),
            rx.text(
                f"Table {reservation['table_number']} • {reservation['start_time']} - {reservation['end_time']}",
                class_name="text-sm text-slate-400"
            ),
            class_name="space-y-0",
            spacing="0"
        ),
        rx.box(
            reservation["status"],
            class_name=f"""
                px-2 py-1 rounded text-xs font-medium text-white
                {status_colors.get(reservation['status'], 'bg-slate-600')}
            """
        ),
        class_name="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg"
    )

def rental_item(rental: Dict[str, Any]) -> rx.Component:
    """Render a rental item."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(f"Table {rental['table_number']}", class_name="font-medium text-white"),
                rx.box("Active", class_name="px-2 py-1 bg-green-600 rounded text-xs font-medium text-white"),
                class_name="flex items-center justify-between mb-2"
            ),
            rx.text(rental["customer_name"], class_name="text-sm text-slate-400"),
            rx.text(
                f"Duration: {rental['duration']}h • ${rental['total_amount']:.2f}",
                class_name="text-sm text-slate-400"
            ),
            rx.text(
                f"Started: {rental['start_time']}",
                class_name="text-xs text-slate-500 mt-1"
            ),
            class_name="space-y-1"
        ),
        class_name="p-4 bg-slate-700/30 rounded-lg"
    )

def quick_action_button(title: str, icon_name: str, color_class: str) -> rx.Component:
    """Create a quick action button."""
    return rx.button(
        rx.vstack(
            rx.icon(tag=icon_name, size=24, class_name=f"mx-auto mb-2 {color_class}"),
            rx.text(title, class_name="text-sm text-white"),
            class_name="space-y-0"
        ),
        class_name=f"""
            p-4 bg-slate-700/50 border border-slate-600/50 rounded-lg 
            hover:bg-slate-700/70 transition-all duration-200
        """
    )

@require_auth
def dashboard_page() -> rx.Component:
    """Dashboard page component."""
    
    # Load data when component mounts
    DashboardState.load_dashboard_data()
    
    return layout(
        rx.vstack(
            # Header
            rx.vstack(
                rx.heading("Amorty & Cafe", class_name="text-4xl font-bold text-white mb-2 text-center"),
                rx.text("Management Dashboard", class_name="text-xl text-slate-400 text-center"),
                class_name="text-center space-y-2"
            ),
            
            # Main Metric Cards
            rx.grid(
                metric_card(
                    "Total Customers",
                    rx.var(DashboardState.total_customers).to_string(),
                    "Registered members",
                    "users",
                    "bg-gradient-to-br from-blue-900/20 via-slate-800/40 to-slate-900/60"
                ),
                metric_card(
                    "Today's Revenue",
                    f"${DashboardState.today_revenue:.2f}",
                    f"From {DashboardState.today_orders} orders",
                    "dollar_sign",
                    "bg-gradient-to-br from-green-900/20 via-slate-800/40 to-slate-900/60"
                ),
                metric_card(
                    "Available Tables",
                    f"{DashboardState.available_tables}/{DashboardState.total_tables}",
                    "Ready for use",
                    "circle_dot",
                    "bg-gradient-to-br from-purple-900/20 via-slate-800/40 to-slate-900/60"
                ),
                metric_card(
                    "Active Rentals",
                    rx.var(DashboardState.active_rentals).to_string(),
                    "Tables in use",
                    "zap",
                    "bg-gradient-to-br from-orange-900/20 via-slate-800/40 to-slate-900/60"
                ),
                columns="4",
                spacing="6",
                class_name="grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            ),
            
            # Secondary Cards
            rx.grid(
                secondary_card(
                    "Staff Members",
                    rx.var(DashboardState.total_employees).to_string(),
                    "Active workforce",
                    "user_check"
                ),
                secondary_card(
                    "Menu Items",
                    rx.var(DashboardState.total_menu_items).to_string(),
                    "Available items",
                    "coffee"
                ),
                secondary_card(
                    "Today's Orders",
                    rx.var(DashboardState.today_orders).to_string(),
                    "Completed today",
                    "shopping_cart"
                ),
                secondary_card(
                    "Pending Reservations",
                    rx.var(DashboardState.pending_reservations).to_string(),
                    "Awaiting confirmation",
                    "calendar"
                ),
                columns="4",
                spacing="6",
                class_name="grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            ),
            
            # Activity Cards
            rx.grid(
                activity_card(
                    "Recent Orders",
                    "shopping_cart",
                    DashboardState.recent_orders,
                    order_item
                ),
                activity_card(
                    "Upcoming Reservations",
                    "calendar",
                    DashboardState.upcoming_reservations,
                    reservation_item
                ),
                columns="2",
                spacing="6",
                class_name="grid-cols-1 lg:grid-cols-2 gap-6"
            ),
            
            # Active Rentals
            rx.cond(
                len(DashboardState.active_rental_list) > 0,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="circle_dot", size=20),
                            rx.heading("Active Table Rentals", class_name="text-white"),
                            class_name="flex items-center"
                        ),
                        rx.grid(
                            *[rental_item(rental) for rental in DashboardState.active_rental_list],
                            columns="3",
                            spacing="4",
                            class_name="grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                        ),
                        class_name="space-y-4"
                    ),
                    class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
                )
            ),
            
            # Quick Actions
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="trending_up", size=20),
                        rx.heading("Quick Actions", class_name="text-white"),
                        class_name="flex items-center"
                    ),
                    rx.grid(
                        quick_action_button("Add Customer", "users", "text-blue-400"),
                        quick_action_button("New Order", "shopping_cart", "text-green-400"),
                        quick_action_button("Make Reservation", "calendar", "text-purple-400"),
                        quick_action_button("Start Rental", "circle_dot", "text-orange-400"),
                        columns="4",
                        spacing="4",
                        class_name="grid-cols-2 md:grid-cols-4 gap-4"
                    ),
                    class_name="space-y-4"
                ),
                class_name="bg-gradient-to-r from-slate-800/50 to-slate-700/50 border-slate-600 rounded-lg p-6"
            ),
            
            class_name="space-y-8"
        )
    )
