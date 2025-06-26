"""Super simple startup for Amorty Cafe."""

print("🎱 Starting Amorty Cafe Management System...")
print("📱 Will open at: http://localhost:3000")
print("🔐 Admin login: admin/admin")
print("👤 Customer login: CUS1, CUS2, etc.")
print("-" * 50)

# Import and run the simple app
from amorty_cafe.simple_app import app

if __name__ == "__main__":
    app.run()
