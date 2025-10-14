#!/usr/bin/env python3
"""
Cross-platform setup script for CPU Scheduling Application
"""

import subprocess
import sys
import os

def check_python():
    """Check if Python is available"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8 or higher is required!")
            print(f"   Current version: {version.major}.{version.minor}")
            return False
        print(f"✅ Python {version.major}.{version.minor} found")
        return True
    except Exception as e:
        print(f"❌ Error checking Python: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install PySide6
        print("   Installing PySide6...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
        print("✅ PySide6 installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    print("=" * 50)
    print("🎯 CPU Scheduling App - Setup Script")
    print("=" * 50)
    
    if not check_python():
        print("\n❌ Setup failed. Please install Python 3.8+ and try again.")
        input("Press Enter to exit...")
        return False
    
    if not install_dependencies():
        print("\n❌ Setup failed. Please check your internet connection.")
        input("Press Enter to exit...")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\n📋 Next steps:")
    if os.name == 'nt':  # Windows
        print("   • Double-click 'run.bat' to start the application")
    print("   • Or run: python main_new.py")
    print("\n✨ Enjoy practicing CPU scheduling algorithms!")
    
    input("\nPress Enter to exit...")
    return True

if __name__ == "__main__":
    main()
