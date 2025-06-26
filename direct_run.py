"""Direct run using reflex command."""
import subprocess
import sys
import os

def main():
    print("🎱 Amorty Cafe Management System")
    print("=" * 40)
    print("📱 Starting on: http://localhost:3000")
    print("🔐 Admin: admin/admin")
    print("👤 Customer: CUS1, CUS2, etc.")
    print("=" * 40)
    
    # Clean any old builds
    if os.path.exists(".web"):
        import shutil
        shutil.rmtree(".web")
        print("🧹 Cleaned old build files")
    
    if os.path.exists(".vite"):
        import shutil
        shutil.rmtree(".vite")
        print("🧹 Cleaned vite cache")
    
    # Change the main app file temporarily
    if os.path.exists("amorty_cafe/amorty_cafe.py"):
        os.rename("amorty_cafe/amorty_cafe.py", "amorty_cafe/amorty_cafe_backup.py")
    
    os.rename("amorty_cafe/simple_app.py", "amorty_cafe/amorty_cafe.py")
    
    try:
        # Run reflex
        subprocess.run([sys.executable, "-m", "reflex", "run"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Restore files
        if os.path.exists("amorty_cafe/amorty_cafe_backup.py"):
            os.rename("amorty_cafe/amorty_cafe.py", "amorty_cafe/simple_app.py")
            os.rename("amorty_cafe/amorty_cafe_backup.py", "amorty_cafe/amorty_cafe.py")

if __name__ == "__main__":
    main()
