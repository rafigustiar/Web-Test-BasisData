"""Run the full admin dashboard."""

print("🎱 Amorty Cafe - Full Admin Dashboard")
print("=" * 50)
print("📱 Will open at: http://localhost:3000")
print("🔐 Admin login: admin/admin")
print("👤 Customer login: CUS1, CUS2, etc.")
print("=" * 50)

# Import and run the full admin app
from amorty_cafe.full_admin_app import app

if __name__ == "__main__":
    app.run()
