"""Simple start script for Amorty Cafe."""
import reflex as rx

# Import our app
from amorty_cafe.amorty_cafe import app

if __name__ == "__main__":
    print("🎱 Starting Amorty Cafe Management System...")
    print("📱 Open browser: http://localhost:3000")
    print("🔐 Admin: username=admin, password=admin")
    print("👤 Customer: gunakan ID seperti CUS1, CUS2")
    
    app.run()
