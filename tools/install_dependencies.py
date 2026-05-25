#!/usr/bin/env python
"""
Install all required dependencies for Invoice Management System
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    print(f"\n{'='*60}")
    print(f"Installing: {package}")
    print('='*60)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--upgrade"],
            cwd=r'd:\shree gopal traders'
        )
        if result.returncode == 0:
            print(f"✅ {package} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def main():
    """Install all dependencies"""
    print("\n" + "="*60)
    print("INSTALLING DEPENDENCIES")
    print("="*60)
    
    packages = [
        "flask",
        "flask-login",
        "reportlab",
        "qrcode[pil]"
    ]
    
    failed = []
    for package in packages:
        if not install_package(package):
            failed.append(package)
    
    print("\n" + "="*60)
    if not failed:
        print("✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
        print("="*60)
        print("\nYou can now run:")
        print("  python app.py")
        print("\nOr use all-in-one startup:")
        print("  python run_all.py")
        return 0
    else:
        print("❌ SOME PACKAGES FAILED TO INSTALL:")
        for pkg in failed:
            print(f"  • {pkg}")
        print("="*60)
        print("\nPlease try installing manually:")
        print(f"  pip install {' '.join(packages)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
