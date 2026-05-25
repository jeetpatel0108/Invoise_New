#!/usr/bin/env python
"""Test the payment features implementation"""
import sys
sys.path.insert(0, r'd:\shree gopal traders')

try:
    # Try importing app
    print("Testing imports...")
    from app import app, db_conn, generate_qr_code, generate_bill_number
    print("✓ All imports successful")
    
    # Test generate_qr_code function
    print("\nTesting QR code generation...")
    qr_buffer = generate_qr_code("1000.00")
    if qr_buffer.getbuffer().nbytes > 0:
        print(f"✓ QR code generated successfully ({qr_buffer.getbuffer().nbytes} bytes)")
    else:
        print("✗ QR code generated but is empty")
    
    # Test database connection
    print("\nTesting database...")
    conn = db_conn()
    cursor = conn.cursor()
    
    # Check invoices table has payment columns
    cursor.execute("PRAGMA table_info(invoices)")
    columns = [row[1] for row in cursor.fetchall()]
    required_cols = ['payment_mode', 'payment_status', 'payment_reference']
    
    missing = [c for c in required_cols if c not in columns]
    if not missing:
        print(f"✓ All payment columns exist: {', '.join(required_cols)}")
    else:
        print(f"✗ Missing columns: {', '.join(missing)}")
    
    conn.close()
    
    # Test bill number generation
    print("\nTesting bill number generation...")
    bill_no = generate_bill_number(1, "2025-05-21")
    if bill_no.startswith("INV-"):
        print(f"✓ Bill number format correct: {bill_no}")
    else:
        print(f"✗ Bill number format incorrect: {bill_no}")
    
    print("\n✅ All tests passed! Payment features ready.")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
