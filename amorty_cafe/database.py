"""Database setup and Oracle integration for Amorty Cafe Management System."""
import cx_Oracle
import os
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import reflex as rx
from .models import *
from datetime import datetime, timedelta
import json

class OracleDatabase:
    """Oracle database connection and management."""

    def __init__(self):
        self.connection_string = self._get_oracle_connection_string()
        self.engine = None
        self.session_maker = None

    def _get_oracle_connection_string(self) -> str:
        """Get Oracle connection string from environment variables."""
        # Default values based on Rafi's configuration
        host = os.getenv("ORACLE_HOST", "localhost")
        port = os.getenv("ORACLE_PORT", "1521")
        service_name = os.getenv("ORACLE_SERVICE_NAME", "xe")
        username = os.getenv("ORACLE_USERNAME", "AMORTY")
        password = os.getenv("ORACLE_PASSWORD", "sys")

        return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}"

    def connect(self):
        """Connect to Oracle database."""
        try:
            self.engine = create_engine(
                self.connection_string,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.session_maker = sessionmaker(bind=self.engine)
            print("✅ Oracle database connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Oracle database: {e}")
            return False

    def create_tables(self):
        """Create all tables in Oracle database."""
        try:
            # Create tables using Reflex models
            rx.Model.metadata.create_all(self.engine)
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False

    def get_session(self):
        """Get database session."""
        if self.session_maker:
            return self.session_maker()
        return None

# Global database instance
oracle_db = OracleDatabase()

def setup_database():
    """Setup database connection and create tables."""
    success = oracle_db.connect()
    if success:
        oracle_db.create_tables()
        seed_sample_data()
    return success

def seed_sample_data():
    """Seed the database with sample data."""
    session = oracle_db.get_session()
    if not session:
        return

    try:
        # Check if data already exists
        if session.query(Customer).first():
            print("Sample data already exists!")
            return

        # Create sample users
        from .auth import AuthState
        auth_state = AuthState()

        admin_user = User(
            username="admin",
            email="admin@amorty.com",
            hashed_password=auth_state.hash_password("admin123"),
            role=UserRole.ADMIN
        )

        customer_user = User(
            username="customer1",
            email="customer@example.com",
            hashed_password=auth_state.hash_password("customer123"),
            role=UserRole.CUSTOMER
        )

        session.add_all([admin_user, customer_user])
        session.commit()

        # Create sample customers
        customers = [
            Customer(
                name="John Doe",
                email="john.doe@email.com",
                phone="+1234567890",
                address="123 Main St, City",
                membership_type=MembershipType.VIP,
                total_spent=1250.0,
                loyalty_points=125,
                user_id=customer_user.id
            ),
            Customer(
                name="Jane Smith",
                email="jane.smith@email.com",
                phone="+1234567891",
                address="456 Oak Ave, City",
                membership_type=MembershipType.REGULAR,
                total_spent=680.0,
                loyalty_points=68
            ),
            Customer(
                name="Mike Johnson",
                email="mike.johnson@email.com",
                phone="+1234567892",
                address="789 Pine Rd, City",
                membership_type=MembershipType.PREMIUM,
                total_spent=2100.0,
                loyalty_points=210
            )
        ]

        # Create sample employees
        employees = [
            Employee(
                name="Alice Brown",
                email="alice.brown@amorty.com",
                phone="+1234567893",
                position="Manager",
                department=Department.MANAGEMENT,
                salary=4500.0,
                hire_date=datetime(2022, 6, 1),
                shift=Shift.MORNING
            ),
            Employee(
                name="Bob Wilson",
                email="bob.wilson@amorty.com",
                phone="+1234567894",
                position="Barista",
                department=Department.CAFE,
                salary=2200.0,
                hire_date=datetime(2023, 2, 15),
                shift=Shift.AFTERNOON
            ),
            Employee(
                name="Carol Davis",
                email="carol.davis@amorty.com",
                phone="+1234567895",
                position="Billiard Attendant",
                department=Department.BILLIARD,
                salary=2000.0,
                hire_date=datetime(2023, 4, 1),
                shift=Shift.NIGHT
            )
        ]

        # Create sample menu items
        menu_items = [
            MenuCafe(
                name="Espresso",
                category=MenuCategory.BEVERAGE,
                price=3.50,
                description="Rich and bold espresso shot",
                ingredients='["Espresso beans", "Water"]',
                preparation_time=2
            ),
            MenuCafe(
                name="Cappuccino",
                category=MenuCategory.BEVERAGE,
                price=4.50,
                description="Espresso with steamed milk and foam",
                ingredients='["Espresso beans", "Milk", "Milk foam"]',
                preparation_time=5
            ),
            MenuCafe(
                name="Club Sandwich",
                category=MenuCategory.FOOD,
                price=8.50,
                description="Triple-layer sandwich with chicken, bacon, and vegetables",
                ingredients='["Bread", "Chicken", "Bacon", "Lettuce", "Tomato", "Mayo"]',
                preparation_time=10
            ),
            MenuCafe(
                name="Chocolate Cake",
                category=MenuCategory.DESSERT,
                price=5.50,
                description="Rich chocolate cake with ganache",
                ingredients='["Chocolate", "Flour", "Sugar", "Eggs", "Butter"]',
                preparation_time=3
            )
        ]

        # Create sample billiard tables
        tables = [
            BilliardTable(
                table_number=1,
                type=TableType.EIGHT_BALL,
                hourly_rate=12.0,
                location="Main Floor - Section A"
            ),
            BilliardTable(
                table_number=2,
                type=TableType.NINE_BALL,
                status=TableStatus.OCCUPIED,
                hourly_rate=15.0,
                location="Main Floor - Section A"
            ),
            BilliardTable(
                table_number=3,
                type=TableType.SNOOKER,
                status=TableStatus.RESERVED,
                hourly_rate=20.0,
                location="VIP Section"
            ),
            BilliardTable(
                table_number=4,
                type=TableType.EIGHT_BALL,
                status=TableStatus.MAINTENANCE,
                hourly_rate=12.0,
                location="Main Floor - Section B",
                condition=TableCondition.NEEDS_REPAIR
            )
        ]

        # Add all sample data
        session.add_all(customers + employees + menu_items + tables)
        session.commit()

        # Create sample orders
        orders = [
            Order(
                customer_id=customers[0].id,
                customer_name=customers[0].name,
                total_amount=16.95,
                status=OrderStatus.SERVED,
                table_number=5,
                notes="Extra hot espresso",
                tax=1.45
            ),
            Order(
                customer_id=customers[1].id,
                customer_name=customers[1].name,
                total_amount=10.90,
                status=OrderStatus.PREPARING,
                table_number=3,
                tax=0.90
            )
        ]

        session.add_all(orders)
        session.commit()

        # Create sample order items
        order_items = [
            OrderItem(
                order_id=orders[0].id,
                menu_id=menu_items[0].id,
                menu_name=menu_items[0].name,
                quantity=2,
                unit_price=3.50,
                subtotal=7.00
            ),
            OrderItem(
                order_id=orders[0].id,
                menu_id=menu_items[2].id,
                menu_name=menu_items[2].name,
                quantity=1,
                unit_price=8.50,
                subtotal=8.50
            ),
            OrderItem(
                order_id=orders[1].id,
                menu_id=menu_items[1].id,
                menu_name=menu_items[1].name,
                quantity=1,
                unit_price=4.50,
                subtotal=4.50
            ),
            OrderItem(
                order_id=orders[1].id,
                menu_id=menu_items[3].id,
                menu_name=menu_items[3].name,
                quantity=1,
                unit_price=5.50,
                subtotal=5.50
            )
        ]

        session.add_all(order_items)
        session.commit()

        print("✅ Sample data seeded successfully!")

    except Exception as e:
        print(f"❌ Failed to seed sample data: {e}")
        session.rollback()
    finally:
        session.close()

def get_oracle_session():
    """Get Oracle database session."""
    return oracle_db.get_session()

# Initialize database on import
if __name__ == "__main__":
    setup_database()
