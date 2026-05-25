#!/usr/bin/env python
"""
All-in-One Startup Script
1. Cleans up unnecessary files
2. Runs full test suite
3. Starts the application
"""
import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r'd:\shree gopal traders')
TOOLS_DIR = PROJECT_ROOT / 'tools'
TESTS_DIR = PROJECT_ROOT / 'tests'

def run_cleanup():
    """Run cleanup and organization"""
    print("\n" + "="*70)
    print("STEP 1: CLEANUP & ORGANIZATION")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, str(TOOLS_DIR / 'cleanup_and_organize.py')],
            cwd=PROJECT_ROOT,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

def run_tests():
    """Run full test suite"""
    print("\n" + "="*70)
    print("STEP 2: RUNNING TEST SUITE")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, str(TESTS_DIR / 'run_all_tests.py')],
            cwd=PROJECT_ROOT,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def run_app():
    """Start the Flask application"""
    print("\n" + "="*70)
    print("STEP 3: STARTING APPLICATION")
    print("="*70)
    
    print("\n✅ Starting Flask application...")
    print("   App URL: http://localhost:5000")
    print("   Press CTRL+C to stop\n")
    
    try:
        os.chdir(PROJECT_ROOT)
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / 'app.py')],
            cwd=PROJECT_ROOT
        )
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped")
        return True
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        return False

def main():
    """Main entry point"""
    print("="*70)
    print("INVOICE MANAGEMENT SYSTEM - STARTUP SCRIPT")
    print("="*70)
    print(f"Project: {PROJECT_ROOT}")
    print(f"Python: {sys.executable}")
    print("="*70)
    
    # Step 1: Cleanup
    if not run_cleanup():
        print("\n⚠ Cleanup had issues but continuing...")
    
    # Step 2: Tests
    if not run_tests():
        response = input("\n⚠ Some tests failed. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Startup cancelled")
            sys.exit(1)
    
    # Step 3: Run app
    run_app()

if __name__ == '__main__':
    main()
