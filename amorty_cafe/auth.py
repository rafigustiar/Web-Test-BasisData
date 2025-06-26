"""Authentication utilities and state management."""
import reflex as rx
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .models import User, UserRole

# JWT Configuration
SECRET_KEY = "your-secret-key-here"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthState(rx.State):
    """Authentication state management."""
    is_authenticated: bool = False
    current_user: Optional[dict] = None
    login_error: str = ""
    signup_error: str = ""
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    async def login(self, username: str, password: str):
        """Login user."""
        try:
            with rx.session() as session:
                user = session.query(User).filter(User.username == username).first()
                
                if user and self.verify_password(password, user.hashed_password) and user.is_active:
                    token = self.create_access_token({"sub": user.username, "role": user.role.value})
                    self.current_user = {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role.value,
                        "token": token
                    }
                    self.is_authenticated = True
                    self.login_error = ""
                    return rx.redirect("/dashboard" if user.role == UserRole.ADMIN else "/customer-dashboard")
                else:
                    self.login_error = "Invalid username or password"
        except Exception as e:
            self.login_error = f"Login failed: {str(e)}"
    
    async def signup(self, username: str, email: str, password: str, role: str = "customer"):
        """Sign up new user."""
        try:
            with rx.session() as session:
                # Check if user exists
                existing_user = session.query(User).filter(
                    (User.username == username) | (User.email == email)
                ).first()
                
                if existing_user:
                    self.signup_error = "Username or email already exists"
                    return
                
                # Create new user
                user_role = UserRole.CUSTOMER if role == "customer" else UserRole.ADMIN
                hashed_pw = self.hash_password(password)
                
                new_user = User(
                    username=username,
                    email=email,
                    hashed_password=hashed_pw,
                    role=user_role
                )
                
                session.add(new_user)
                session.commit()
                
                self.signup_error = ""
                return rx.redirect("/login")
                
        except Exception as e:
            self.signup_error = f"Signup failed: {str(e)}"
    
    def logout(self):
        """Logout user."""
        self.is_authenticated = False
        self.current_user = None
        return rx.redirect("/login")
    
    def check_auth(self):
        """Check if user is authenticated."""
        return self.is_authenticated
    
    def check_admin(self):
        """Check if user is admin."""
        return self.is_authenticated and self.current_user and self.current_user.get("role") == "admin"

def require_auth(func):
    """Decorator to require authentication."""
    def wrapper(*args, **kwargs):
        auth_state = AuthState()
        if not auth_state.check_auth():
            return rx.redirect("/login")
        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    """Decorator to require admin role."""
    def wrapper(*args, **kwargs):
        auth_state = AuthState()
        if not auth_state.check_admin():
            return rx.redirect("/login")
        return func(*args, **kwargs)
    return wrapper
