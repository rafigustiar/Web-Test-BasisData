"""Authentication utilities and state management for Rafi's system."""
import reflex as rx
from typing import Optional

class AuthState(rx.State):
    """Simple authentication state management."""
    is_authenticated: bool = False
    current_user: Optional[dict] = None
    login_error: str = ""
    user_role: str = ""  # "admin" or "customer"
    
    def login_admin(self, username: str, password: str):
        """Login as admin."""
        self.login_error = ""
        
        # Simple admin login - hardcoded for now
        if username == "admin" and password == "admin":
            self.is_authenticated = True
            self.user_role = "admin"
            self.current_user = {
                "username": username,
                "role": "admin"
            }
            return rx.redirect("/admin-dashboard")
        else:
            self.login_error = "Username atau password admin salah!"
    
    def login_customer(self, customer_id: str):
        """Login as customer with Customer ID."""
        self.login_error = ""
        
        # Simple customer login - just check if ID format is correct
        if customer_id and customer_id.startswith("CUS"):
            self.is_authenticated = True
            self.user_role = "customer"
            self.current_user = {
                "customer_id": customer_id,
                "role": "customer"
            }
            return rx.redirect("/customer-dashboard")
        else:
            self.login_error = "Customer ID tidak valid! Gunakan format CUS1, CUS2, dll."
    
    def logout(self):
        """Logout current user."""
        self.is_authenticated = False
        self.current_user = None
        self.user_role = ""
        self.login_error = ""
        return rx.redirect("/login")
    
    def check_admin_auth(self):
        """Check if current user is admin."""
        return self.is_authenticated and self.user_role == "admin"
    
    def check_customer_auth(self):
        """Check if current user is customer."""
        return self.is_authenticated and self.user_role == "customer"
