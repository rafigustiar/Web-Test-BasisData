"""Database models for Amorty Cafe Management System."""
import reflex as rx
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MembershipType(Enum):
    REGULAR = "Regular"
    VIP = "VIP"
    PREMIUM = "Premium"

class CustomerStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class EmployeeStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ON_LEAVE = "On Leave"

class Department(Enum):
    CAFE = "Cafe"
    BILLIARD = "Billiard"
    MANAGEMENT = "Management"
    MAINTENANCE = "Maintenance"

class Shift(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"

class MenuCategory(Enum):
    FOOD = "Food"
    BEVERAGE = "Beverage"
    SNACK = "Snack"
    DESSERT = "Dessert"

class TableType(Enum):
    EIGHT_BALL = "8-Ball"
    NINE_BALL = "9-Ball"
    SNOOKER = "Snooker"
    CAROM = "Carom"

class TableStatus(Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"

class TableCondition(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    NEEDS_REPAIR = "Needs Repair"

class OrderStatus(Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    READY = "Ready"
    SERVED = "Served"
    CANCELLED = "Cancelled"

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    DIGITAL_WALLET = "Digital Wallet"
    BANK_TRANSFER = "Bank Transfer"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class ReservationStatus(Enum):
    CONFIRMED = "Confirmed"
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    NO_SHOW = "No Show"

class RentalStatus(Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    CANCELLED = "Cancelled"

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

# Database Models
class User(rx.Model, table=True):
    """User authentication model."""
    username: str
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = datetime.now()

class Customer(rx.Model, table=True):
    """Customer model."""
    name: str
    email: str
    phone: str
    address: str
    membership_type: MembershipType = MembershipType.REGULAR
    join_date: datetime = datetime.now()
    total_spent: float = 0.0
    loyalty_points: int = 0
    status: CustomerStatus = CustomerStatus.ACTIVE
    user_id: Optional[int] = None

class Employee(rx.Model, table=True):
    """Employee model."""
    name: str
    email: str
    phone: str
    position: str
    department: Department
    salary: float
    hire_date: datetime
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    shift: Shift

class MenuCafe(rx.Model, table=True):
    """Menu item model."""
    name: str
    category: MenuCategory
    price: float
    description: str
    ingredients: str  # JSON string of list
    availability: bool = True
    preparation_time: int  # in minutes
    image_url: Optional[str] = None

class BilliardTable(rx.Model, table=True):
    """Billiard table model."""
    table_number: int
    type: TableType
    status: TableStatus = TableStatus.AVAILABLE
    hourly_rate: float
    location: str
    condition: TableCondition = TableCondition.GOOD

class Order(rx.Model, table=True):
    """Order model."""
    customer_id: int
    customer_name: str
    total_amount: float
    order_date: datetime = datetime.now()
    status: OrderStatus = OrderStatus.PENDING
    table_number: Optional[int] = None
    notes: Optional[str] = None
    discount: float = 0.0
    tax: float = 0.0

class OrderItem(rx.Model, table=True):
    """Order item model."""
    order_id: int
    menu_id: int
    menu_name: str
    quantity: int
    unit_price: float
    subtotal: float
    special_instructions: Optional[str] = None

class Payment(rx.Model, table=True):
    """Payment model."""
    order_id: int
    amount: float
    payment_method: PaymentMethod
    payment_date: datetime = datetime.now()
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    cashier_name: str
    change: Optional[float] = None

class Reservation(rx.Model, table=True):
    """Reservation model."""
    customer_id: int
    customer_name: str
    customer_phone: str
    table_id: int
    table_number: int
    reservation_date: datetime
    start_time: str
    end_time: str
    duration: float  # in hours
    status: ReservationStatus = ReservationStatus.PENDING
    party_size: int
    special_requests: Optional[str] = None
    deposit: float

class RentalTransaction(rx.Model, table=True):
    """Rental transaction model."""
    customer_id: int
    customer_name: str
    table_id: int
    table_number: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: float = 0.0
    hourly_rate: float
    total_amount: float
    status: RentalStatus = RentalStatus.ACTIVE
    additional_services: str = "[]"  # JSON string
    employee_id: int
    employee_name: str
    payment_status: str = "Unpaid"
