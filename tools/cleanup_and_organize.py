#!/usr/bin/env python
"""
Project cleanup and organization script
Removes unnecessary files and verifies structure
"""
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(r'd:\shree gopal traders')

# Files to remove (temporary, duplicates, unnecessary)
FILES_TO_DELETE = [
    'tempCodeRunnerFile.python',
    'check_syntax.py',
    'test_fixes.py',
    'CLEANUP.bat',
    '_README_DOCS.txt',
    'COMPLETE_DOCUMENTATION.md',
    'FIXES_SUMMARY.md',
    'FIXES_VISUAL_SUMMARY.txt',
    'IMPLEMENTATION_COMPLETE.txt',
    'QUICK_FIX_GUIDE.txt',
    'PROJECT_STRUCTURE.md',
]

# Files to keep (documentation)
DOCS_TO_KEEP = [
    'PAYMENT_IMPLEMENTATION_SUMMARY.md',
    'QUICK_START_PAYMENT_FEATURES.md',
    'PAYMENT_SYSTEM_README.md',
    'PAYMENT_FEATURES_COMPLETE.md',
    'PAYMENT_SYSTEM_IMPLEMENTATION.md',
    'PAYMENT_IMPLEMENTATION_CHECKLIST.md',
    'README.md',
]

def cleanup():
    print("🧹 Cleaning up unnecessary files...\n")
    
    deleted = []
    for file in FILES_TO_DELETE:
        filepath = PROJECT_ROOT / file
        if filepath.exists():
            try:
                filepath.unlink()
                deleted.append(file)
                print(f"✓ Deleted: {file}")
            except Exception as e:
                print(f"✗ Failed to delete {file}: {e}")
    
    # Delete temp file in modules
    modules_temp = PROJECT_ROOT / 'modules' / 'tempCodeRunnerFile.py'
    if modules_temp.exists():
        try:
            modules_temp.unlink()
            deleted.append('modules/tempCodeRunnerFile.py')
            print(f"✓ Deleted: modules/tempCodeRunnerFile.py")
        except Exception as e:
            print(f"✗ Failed to delete modules temp file: {e}")
    
    print(f"\n✓ Cleaned up {len(deleted)} files")
    
    # Clean __pycache__ directories
    print("\n🧹 Cleaning __pycache__ directories...")
    for pycache in PROJECT_ROOT.rglob('__pycache__'):
        try:
            shutil.rmtree(pycache)
            print(f"✓ Removed: {pycache.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"✗ Failed to remove {pycache}: {e}")

def verify_structure():
    print("\n📁 Verifying project structure...\n")
    
    required_dirs = ['templates', 'static', 'modules', 'generated_pdfs']
    required_files = ['app.py', 'invoice.db', '.env']
    
    print("📂 Directories:")
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ MISSING: {dir_name}/")
    
    print("\n📄 Core Files:")
    for file_name in required_files:
        file_path = PROJECT_ROOT / file_name
        if file_path.exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ MISSING: {file_name}")
    
    print("\n📚 Documentation Files:")
    for doc in DOCS_TO_KEEP:
        doc_path = PROJECT_ROOT / doc
        if doc_path.exists():
            print(f"  ✓ {doc}")
        else:
            print(f"  ⚠ {doc}")

def list_structure():
    print("\n📋 Project Structure:\n")
    
    print("📦 Root Files:")
    for file in sorted(PROJECT_ROOT.glob('*.py')):
        size = file.stat().st_size / 1024
        print(f"  • {file.name} ({size:.1f} KB)")
    
    print("\n📚 Documentation:")
    for file in sorted(PROJECT_ROOT.glob('*.md')):
        print(f"  • {file.name}")
    
    print("\n📁 static/")
    for file in sorted((PROJECT_ROOT / 'static').glob('*')):
        if file.is_file():
            print(f"  • {file.name}")
    
    print("\n📁 templates/")
    for file in sorted((PROJECT_ROOT / 'templates').glob('*.html')):
        print(f"  • {file.name}")
    
    print("\n📁 modules/")
    for file in sorted((PROJECT_ROOT / 'modules').glob('*.py')):
        if file.name != '__pycache__':
            print(f"  • {file.name}")

if __name__ == '__main__':
    try:
        cleanup()
        verify_structure()
        list_structure()
        print("\n" + "="*50)
        print("✅ Cleanup and organization complete!")
        print("="*50)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
