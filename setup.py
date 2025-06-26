"""Setup script for Amorty Cafe Management System."""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Amorty Cafe Management System...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Creating environment file")
            print("📝 Please edit .env file with your Oracle database credentials")
        else:
            print("⚠️  .env.example not found, please create .env manually")
    
    # Initialize Reflex
    if not run_command("reflex init", "Initializing Reflex"):
        print("⚠️  Reflex initialization failed, but continuing...")
    
    print("=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Oracle database credentials")
    print("2. Setup Oracle database and create user/schema")
    print("3. Run: python -c \"from amorty_cafe.database import setup_database; setup_database()\"")
    print("4. Run: reflex run")
    print("\n🔗 Application will be available at: http://localhost:3000")
    print("🔐 Default login: admin/admin123 or customer1/customer123")

if __name__ == "__main__":
    main()
