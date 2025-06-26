"""Enhanced main entry point for Rafi's Amorty Cafe Management System."""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import after setting up path and env
from amorty_cafe.database_rafi import setup_database_rafi
from amorty_cafe.amorty_cafe import app

def main():
    """Main application entry point."""
    print("🎱 Amorty Cafe Management System")
    print("=" * 40)
    print("Starting application...")
    
    # Setup database if needed
    if "--setup-db" in sys.argv:
        print("\n🗄️  Setting up database...")
        if setup_database_rafi():
            print("✅ Database setup completed!")
        else:
            print("❌ Database setup failed!")
            return
    
    # Run the Reflex app
    print("\n🚀 Starting Reflex application...")
    print("📱 Application will be available at: http://localhost:3000")
    print("🔐 Login credentials:")
    print("   👑 Admin: username=admin, password=admin")
    print("   👤 Customer: ID Customer dari database (contoh: CUS1, CUS2, CUS3)")
    print("\n" + "=" * 40)
    
    app.run()

if __name__ == "__main__":
    main()
