#!/usr/bin/env python
"""
Complete test suite for Invoice Management System with Payment Features
Tests: Imports, Database, Functions, Routes, Features
"""
import sys
import os
sys.path.insert(0, r'd:\shree gopal traders')

def test_imports():
    """Test all required imports"""
    print("\n" + "="*60)
    print("🧪 TEST 1: IMPORTS")
    print("="*60)
    
    try:
        print("Testing Flask imports...")
        from flask import Flask, render_template, request, send_file
        print("  ✓ Flask imported")
        
        print("Testing database imports...")
        import sqlite3
        print("  ✓ SQLite3 imported")
        
        print("Testing reportlab imports...")
        from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        print("  ✓ ReportLab imported")
        
        print("Testing payment feature imports...")
        import qrcode
        import io
        print("  ✓ QRCode imported")
        print("  ✓ IO imported")
        
        print("Testing app import...")
        from app import app, db_conn, generate_qr_code, generate_bill_number
        print("  ✓ App imported successfully")
        
        print("\n✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        return False

def test_database():
    """Test database connectivity and schema"""
    print("\n" + "="*60)
    print("🧪 TEST 2: DATABASE")
    print("="*60)
    
    try:
        from app import db_conn
        
        print("Connecting to database...")
        conn = db_conn()
        print("  ✓ Connected to invoice.db")
        
        cursor = conn.cursor()
        
        print("\nChecking tables...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'invoices', 'items']
        for table in required_tables:
            if table in tables:
                print(f"  ✓ Table '{table}' exists")
            else:
                print(f"  ✗ Table '{table}' MISSING")
        
        print("\nChecking invoices table schema...")
        cursor.execute("PRAGMA table_info(invoices)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        required_columns = {
            'id': 'int',
            'user_id': 'int',
            'customer': 'text',
            'phone': 'text',
            'date': 'text',
            'bill_number': 'text',
            'payment_mode': 'text',
            'payment_status': 'text',
            'payment_reference': 'text'
        }
        
        for col, dtype in required_columns.items():
            if col in columns:
                print(f"  ✓ Column '{col}' exists")
            else:
                print(f"  ✗ Column '{col}' MISSING")
        
        conn.close()
        print("\n✅ Database check complete!")
        return True
    except Exception as e:
        print(f"\n❌ Database Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functions():
    """Test core functions"""
    print("\n" + "="*60)
    print("🧪 TEST 3: CORE FUNCTIONS")
    print("="*60)
    
    try:
        from app import generate_qr_code, generate_bill_number, db_conn
        
        print("Testing generate_bill_number()...")
        bill_no = generate_bill_number(1, "2025-05-22")
        if bill_no.startswith("INV-"):
            print(f"  ✓ Bill number generated: {bill_no}")
        else:
            print(f"  ✗ Invalid bill number format: {bill_no}")
            return False
        
        print("\nTesting generate_qr_code()...")
        qr_buffer = generate_qr_code("1000.00")
        if qr_buffer.getbuffer().nbytes > 0:
            size_kb = qr_buffer.getbuffer().nbytes / 1024
            print(f"  ✓ QR code generated ({size_kb:.2f} KB)")
        else:
            print("  ✗ QR code is empty")
            return False
        
        print("\nTesting db_conn()...")
        conn = db_conn()
        if conn:
            print("  ✓ Database connection successful")
            conn.close()
        else:
            print("  ✗ Database connection failed")
            return False
        
        print("\n✅ All functions working!")
        return True
    except Exception as e:
        print(f"\n❌ Function Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app():
    """Test Flask app"""
    print("\n" + "="*60)
    print("🧪 TEST 4: FLASK APPLICATION")
    print("="*60)
    
    try:
        from app import app
        
        print("Checking Flask app...")
        if app:
            print("  ✓ Flask app created")
        
        print("\nChecking routes...")
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(rule.rule)
        
        required_routes = ['/', '/login', '/register', '/logout', '/create', 
                          '/download/<int:id>', '/invoices', '/unpaid-bills', '/mark-paid/<int:id>']
        
        for route in required_routes:
            if any(route in r for r in routes):
                print(f"  ✓ Route {route} exists")
            else:
                print(f"  ⚠ Route {route} may be missing")
        
        print(f"\n  Total routes registered: {len(routes)}")
        
        print("\n✅ Flask app check complete!")
        return True
    except Exception as e:
        print(f"\n❌ App Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_payment_features():
    """Test payment features"""
    print("\n" + "="*60)
    print("🧪 TEST 5: PAYMENT FEATURES")
    print("="*60)
    
    try:
        from app import db_conn
        
        conn = db_conn()
        cursor = conn.cursor()
        
        print("Checking payment_mode column...")
        cursor.execute("PRAGMA table_info(invoices)")
        columns = [row[1] for row in cursor.fetchall()]
        
        payment_cols = ['payment_mode', 'payment_status', 'payment_reference', 'payment_date']
        all_present = True
        
        for col in payment_cols:
            if col in columns:
                print(f"  ✓ Column '{col}' exists")
            else:
                print(f"  ✗ Column '{col}' MISSING")
                all_present = False
        
        print("\nTesting payment defaults...")
        cursor.execute("PRAGMA table_info(invoices)")
        for row in cursor.fetchall():
            if row[1] == 'payment_mode' and row[4] == 'CASH':
                print(f"  ✓ payment_mode defaults to CASH")
            elif row[1] == 'payment_status' and row[4] == 'UNPAID':
                print(f"  ✓ payment_status defaults to UNPAID")
        
        conn.close()
        
        if all_present:
            print("\n✅ Payment features ready!")
            return True
        else:
            print("\n⚠ Some payment features missing")
            return False
    except Exception as e:
        print(f"\n❌ Payment Features Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test template files"""
    print("\n" + "="*60)
    print("🧪 TEST 6: TEMPLATE FILES")
    print("="*60)
    
    try:
        from pathlib import Path
        
        template_dir = Path(r'd:\shree gopal traders\templates')
        
        required_templates = [
            'login.html',
            'register.html',
            'index.html',
            'create.html',
            'invoices.html',
            'unpaid_bills.html',
            'success.html',
            'welcome.html',
            'forgot_password.html'
        ]
        
        print("Checking template files...")
        all_present = True
        for template in required_templates:
            template_path = template_dir / template
            if template_path.exists():
                size_kb = template_path.stat().st_size / 1024
                print(f"  ✓ {template} ({size_kb:.1f} KB)")
            else:
                print(f"  ✗ {template} MISSING")
                all_present = False
        
        if all_present:
            print("\n✅ All templates present!")
        else:
            print("\n⚠ Some templates missing")
        
        return all_present
    except Exception as e:
        print(f"\n❌ Template Test Error: {e}")
        return False

def test_static_files():
    """Test static files"""
    print("\n" + "="*60)
    print("🧪 TEST 7: STATIC FILES")
    print("="*60)
    
    try:
        from pathlib import Path
        
        static_dir = Path(r'd:\shree gopal traders\static')
        
        required_files = ['style.css', 'themes.css', 'forms.js']
        
        print("Checking static files...")
        all_present = True
        for file in required_files:
            file_path = static_dir / file
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                print(f"  ✓ {file} ({size_kb:.1f} KB)")
            else:
                print(f"  ✗ {file} MISSING")
                all_present = False
        
        if all_present:
            print("\n✅ All static files present!")
        else:
            print("\n⚠ Some static files missing")
        
        return all_present
    except Exception as e:
        print(f"\n❌ Static Files Test Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("INVOICE MANAGEMENT SYSTEM - COMPLETE TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Functions", test_functions()))
    results.append(("Flask App", test_app()))
    results.append(("Payment Features", test_payment_features()))
    results.append(("Templates", test_templates()))
    results.append(("Static Files", test_static_files()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - SYSTEM READY!")
    else:
        print("⚠ Some tests failed - review above")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
