#!/usr/bin/env python3
"""Simple startup script for Amorty Cafe Management System."""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main startup function."""
    print("🎱 Amorty Cafe Management System")
    print("=" * 50)
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("📋 Creating .env file from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ .env file created! Please update it with your database credentials.")
        else:
            print("❌ .env.example not found!")
            return
    
    # Check if dependencies are installed
    try:
        import reflex
        print("✅ Reflex is installed")
    except ImportError:
        print("❌ Reflex not installed. Please run: pip install -r requirements.txt")
        return
    
    # Try to run the application
    try:
        print("\n🚀 Starting Amorty Cafe Management System...")
        print("📱 Open your browser and go to: http://localhost:3000")
        print("🔐 Login credentials:")
        print("   👑 Admin: username=admin, password=admin")
        print("   👤 Customer: Use any Customer ID from database")
        print("\n" + "=" * 50)
        
        # Use reflex run command directly
        subprocess.run([sys.executable, "-m", "reflex", "run", "--env", "dev"], check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have installed dependencies: pip install -r requirements.txt")
        print("2. Check your .env file has correct database credentials")
        print("3. Ensure Oracle client is properly installed and configured")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
