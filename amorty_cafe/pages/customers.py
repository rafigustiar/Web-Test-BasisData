"""Customer management page for Amorty Cafe Management System."""
import reflex as rx
from typing import List, Dict, Any
from ..components.layout import layout
from ..auth import AuthState, require_admin
from ..models import Customer, MembershipType, CustomerStatus
import json

class CustomerState(rx.State):
    """Customer management state."""
    customers: List[Dict[str, Any]] = []
    is_dialog_open: bool = False
    editing_customer: Dict[str, Any] = {}
    form_data: Dict[str, Any] = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "membership_type": "Regular",
        "total_spent": 0.0,
        "loyalty_points": 0
    }
    
    async def load_customers(self):
        """Load customers from database."""
        with rx.session() as session:
            customers = session.query(Customer).all()
            self.customers = [
                {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address,
                    "membership_type": customer.membership_type.value,
                    "join_date": customer.join_date.strftime("%Y-%m-%d"),
                    "total_spent": customer.total_spent,
                    "loyalty_points": customer.loyalty_points,
                    "status": customer.status.value
                }
                for customer in customers
            ]
    
    def open_add_dialog(self):
        """Open dialog for adding new customer."""
        self.editing_customer = {}
        self.form_data = {
            "name": "",
            "email": "",
            "phone": "",
            "address": "",
            "membership_type": "Regular",
            "total_spent": 0.0,
            "loyalty_points": 0
        }
        self.is_dialog_open = True
    
    def open_edit_dialog(self, customer: Dict[str, Any]):
        """Open dialog for editing customer."""
        self.editing_customer = customer
        self.form_data = {
            "name": customer["name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "address": customer["address"],
            "membership_type": customer["membership_type"],
            "total_spent": customer["total_spent"],
            "loyalty_points": customer["loyalty_points"]
        }
        self.is_dialog_open = True
    
    def close_dialog(self):
        """Close dialog."""
        self.is_dialog_open = False
        self.editing_customer = {}
    
    def set_form_field(self, field: str, value: str):
        """Set form field value."""
        self.form_data[field] = value
    
    async def save_customer(self):
        """Save customer to database."""
        with rx.session() as session:
            if self.editing_customer:
                # Update existing customer
                customer = session.query(Customer).filter(Customer.id == self.editing_customer["id"]).first()
                if customer:
                    customer.name = self.form_data["name"]
                    customer.email = self.form_data["email"]
                    customer.phone = self.form_data["phone"]
                    customer.address = self.form_data["address"]
                    customer.membership_type = MembershipType(self.form_data["membership_type"])
                    customer.total_spent = float(self.form_data["total_spent"])
                    customer.loyalty_points = int(self.form_data["loyalty_points"])
            else:
                # Create new customer
                customer = Customer(
                    name=self.form_data["name"],
                    email=self.form_data["email"],
                    phone=self.form_data["phone"],
                    address=self.form_data["address"],
                    membership_type=MembershipType(self.form_data["membership_type"]),
                    total_spent=float(self.form_data["total_spent"]),
                    loyalty_points=int(self.form_data["loyalty_points"])
                )
                session.add(customer)
            
            session.commit()
            self.close_dialog()
            await self.load_customers()
    
    async def delete_customer(self, customer_id: int):
        """Delete customer from database."""
        with rx.session() as session:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                session.delete(customer)
                session.commit()
                await self.load_customers()

def membership_badge(membership_type: str) -> rx.Component:
    """Create membership badge."""
    colors = {
        "Regular": "bg-slate-600",
        "VIP": "bg-yellow-600",
        "Premium": "bg-purple-600"
    }
    
    icons = {
        "Regular": "users",
        "VIP": "star",
        "Premium": "award"
    }
    
    return rx.box(
        rx.hstack(
            rx.icon(tag=icons.get(membership_type, "users"), size=12),
            rx.text(membership_type, class_name="text-white text-xs font-medium"),
            class_name="flex items-center space-x-1"
        ),
        class_name=f"px-2 py-1 rounded {colors.get(membership_type, 'bg-slate-600')}"
    )

def customer_row(customer: Dict[str, Any]) -> rx.Component:
    """Create customer table row."""
    return rx.tr(
        rx.td(customer["name"], class_name="text-slate-200 py-4 px-4"),
        rx.td(customer["email"], class_name="text-slate-200 py-4 px-4"),
        rx.td(customer["phone"], class_name="text-slate-200 py-4 px-4"),
        rx.td(
            membership_badge(customer["membership_type"]),
            class_name="text-slate-200 py-4 px-4"
        ),
        rx.td(
            f"${customer['total_spent']:,.2f}",
            class_name="text-slate-200 py-4 px-4"
        ),
        rx.td(
            rx.box(
                f"{customer['loyalty_points']} pts",
                class_name="px-2 py-1 bg-blue-600/20 border border-blue-400/30 rounded text-blue-400 text-xs"
            ),
            class_name="text-slate-200 py-4 px-4"
        ),
        rx.td(
            customer["join_date"],
            class_name="text-slate-200 py-4 px-4"
        ),
        rx.td(
            rx.hstack(
                rx.button(
                    rx.icon(tag="edit", size=16),
                    on_click=lambda: CustomerState.open_edit_dialog(customer),
                    class_name="h-8 w-8 p-0 text-slate-400 hover:text-yellow-400 bg-transparent border-none",
                    variant="ghost"
                ),
                rx.button(
                    rx.icon(tag="trash_2", size=16),
                    on_click=lambda: CustomerState.delete_customer(customer["id"]),
                    class_name="h-8 w-8 p-0 text-slate-400 hover:text-red-400 bg-transparent border-none",
                    variant="ghost"
                ),
                class_name="flex items-center space-x-2"
            ),
            class_name="text-slate-200 py-4 px-4"
        ),
        class_name="border-slate-700 hover:bg-slate-700/20 transition-colors"
    )

def customer_form() -> rx.Component:
    """Customer form dialog."""
    return rx.cond(
        CustomerState.is_dialog_open,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                CustomerState.editing_customer,
                                "Edit Customer",
                                "Add New Customer"
                            ),
                            class_name="text-white text-xl font-semibold"
                        ),
                        rx.button(
                            rx.icon(tag="x", size=20),
                            on_click=CustomerState.close_dialog,
                            class_name="text-slate-400 hover:text-white bg-transparent border-none",
                            variant="ghost"
                        ),
                        class_name="flex justify-between items-center w-full"
                    ),
                    
                    rx.vstack(
                        # Name field
                        rx.vstack(
                            rx.text("Full Name", class_name="text-sm font-medium text-slate-300"),
                            rx.input(
                                placeholder="Enter full name",
                                value=CustomerState.form_data["name"],
                                on_change=lambda value: CustomerState.set_form_field("name", value),
                                class_name="bg-slate-700 border-slate-600 text-white",
                                required=True
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Email field
                        rx.vstack(
                            rx.text("Email", class_name="text-sm font-medium text-slate-300"),
                            rx.input(
                                placeholder="Enter email address",
                                type="email",
                                value=CustomerState.form_data["email"],
                                on_change=lambda value: CustomerState.set_form_field("email", value),
                                class_name="bg-slate-700 border-slate-600 text-white",
                                required=True
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Phone field
                        rx.vstack(
                            rx.text("Phone", class_name="text-sm font-medium text-slate-300"),
                            rx.input(
                                placeholder="Enter phone number",
                                value=CustomerState.form_data["phone"],
                                on_change=lambda value: CustomerState.set_form_field("phone", value),
                                class_name="bg-slate-700 border-slate-600 text-white",
                                required=True
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Membership Type
                        rx.vstack(
                            rx.text("Membership Type", class_name="text-sm font-medium text-slate-300"),
                            rx.select(
                                ["Regular", "VIP", "Premium"],
                                value=CustomerState.form_data["membership_type"],
                                on_change=lambda value: CustomerState.set_form_field("membership_type", value),
                                class_name="bg-slate-700 border-slate-600 text-white"
                            ),
                            class_name="space-y-1"
                        ),
                        
                        # Address field
                        rx.vstack(
                            rx.text("Address", class_name="text-sm font-medium text-slate-300"),
                            rx.text_area(
                                placeholder="Enter address",
                                value=CustomerState.form_data["address"],
                                on_change=lambda value: CustomerState.set_form_field("address", value),
                                class_name="bg-slate-700 border-slate-600 text-white",
                                rows=3
                            ),
                            class_name="space-y-1"
                        ),
                        
                        class_name="space-y-4 w-full"
                    ),
                    
                    # Action buttons
                    rx.hstack(
                        rx.button(
                            "Cancel",
                            on_click=CustomerState.close_dialog,
                            class_name="border-slate-600 text-slate-300 hover:bg-slate-700",
                            variant="outline"
                        ),
                        rx.button(
                            rx.cond(
                                CustomerState.editing_customer,
                                "Update Customer",
                                "Add Customer"
                            ),
                            on_click=CustomerState.save_customer,
                            class_name="bg-blue-600 hover:bg-blue-700 text-white"
                        ),
                        class_name="flex justify-end space-x-2 pt-4"
                    ),
                    
                    class_name="space-y-6"
                ),
                class_name="bg-slate-800 border-slate-700 text-white max-w-2xl w-full rounded-lg p-8"
            ),
            class_name="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        )
    )

@require_admin
def customers_page() -> rx.Component:
    """Customers management page."""
    
    # Load data when component mounts
    CustomerState.load_customers()
    
    return layout(
        rx.vstack(
            rx.vstack(
                rx.heading("Customer Management", class_name="text-3xl font-bold text-white"),
                rx.text("Manage your customer database and memberships", class_name="text-slate-400"),
                class_name="space-y-2"
            ),
            
            # Data table
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Customers", class_name="text-2xl font-bold text-white"),
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="search", size=16, class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"),
                                rx.input(
                                    placeholder="Search customers...",
                                    class_name="pl-10 bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 w-64"
                                ),
                                class_name="relative"
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="plus", size=16),
                                    rx.text("Add Customer"),
                                    class_name="flex items-center space-x-2"
                                ),
                                on_click=CustomerState.open_add_dialog,
                                class_name="bg-blue-600 hover:bg-blue-700 text-white"
                            ),
                            class_name="flex items-center space-x-4"
                        ),
                        class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0"
                    ),
                    
                    rx.box(
                        rx.table(
                            rx.thead(
                                rx.tr(
                                    rx.th("Name", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Email", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Phone", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Membership", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Total Spent", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Loyalty Points", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Join Date", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    rx.th("Actions", class_name="text-slate-300 font-semibold text-left py-3 px-4"),
                                    class_name="bg-slate-700/30 border-slate-700"
                                )
                            ),
                            rx.tbody(
                                rx.foreach(
                                    CustomerState.customers,
                                    customer_row
                                )
                            ),
                            class_name="w-full"
                        ),
                        class_name="rounded-md border border-slate-700 overflow-hidden"
                    ),
                    
                    rx.cond(
                        len(CustomerState.customers) > 0,
                        rx.hstack(
                            rx.text(
                                f"Showing {len(CustomerState.customers)} customers",
                                class_name="text-sm text-slate-400"
                            ),
                            rx.text(
                                f"Total: {len(CustomerState.customers)} records",
                                class_name="text-sm text-slate-400"
                            ),
                            class_name="flex justify-between items-center mt-4"
                        ),
                        rx.text(
                            "No customers found.",
                            class_name="text-center text-slate-400 py-8"
                        )
                    ),
                    
                    class_name="space-y-4"
                ),
                class_name="bg-slate-800/50 border-slate-700 rounded-lg p-6"
            ),
            
            customer_form(),
            
            class_name="space-y-6"
        )
    )
