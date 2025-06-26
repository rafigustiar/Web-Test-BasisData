#!/usr/bin/env python3
"""Simple startup script for Amorty Cafe Management System."""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import reflex
        print("✅ Reflex is available")
        return True
    except ImportError:
        print("❌ Reflex not installed!")
        print("💡 Install it with: pip install reflex")
        return False

def main():
    """Main startup function."""
    print("🎱 Amorty Cafe Management System")
    print("=" * 50)

    # Ensure we're in the right directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")

    # Check dependencies
    if not check_dependencies():
        return

    # Initialize Reflex if needed
    try:
        print("🔧 Initializing Reflex...")
        result = subprocess.run([sys.executable, "-m", "reflex", "init"],
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0 and "already initialized" not in result.stderr:
            print(f"⚠️ Reflex init warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Reflex init issue: {e}")

    # Try to run the application
    try:
        print("\n🚀 Starting Amorty Cafe Management System...")
        print("📱 Application will open at: http://localhost:3000")
        print("🔐 Login credentials:")
        print("   👑 Admin: username=admin, password=admin")
        print("   👤 Customer: gunakan ID seperti CUS1, CUS2, dll")
        print("\n" + "=" * 50)

        # Use reflex run command
        subprocess.run([sys.executable, "-m", "reflex", "run"], check=True)

    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Install dependencies: pip install reflex")
        print("2. Make sure no other app is using port 3000")
        print("3. Try running: reflex run")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
