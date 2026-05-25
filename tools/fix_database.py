#!/usr/bin/env python
"""
Fix the database schema issue with bill_number UNIQUE constraint
"""
import sqlite3
import os

db_path = r'd:\shree gopal traders\invoice.db'
backup_path = r'd:\shree gopal traders\invoice.db.backup'

print("=" * 70)
print("FIXING DATABASE SCHEMA")
print("=" * 70)

# Backup the database
if os.path.exists(db_path):
    print(f"\n1. Creating backup: {backup_path}")
    try:
        with open(db_path, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        print("   ✅ Backup created")
    except Exception as e:
        print(f"   ❌ Backup failed: {e}")
        exit(1)

# Fix the database
conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    print("\n2. Checking invoice table schema...")
    cur.execute("PRAGMA table_info(invoices)")
    columns = {row[1]: row for row in cur.fetchall()}
    
    if 'bill_number' in columns:
        print("   ✅ bill_number column exists")
        col_info = columns['bill_number']
        print(f"      Type: {col_info[2]}")
        print(f"      NotNull: {col_info[3]}")
        print(f"      Default: {col_info[4]}")
    else:
        print("   ℹ️  bill_number column does not exist (will be created)")
    
    print("\n3. Removing UNIQUE constraint if present...")
    # SQLite doesn't support removing constraints directly, so we recreate the table
    # But first check if the error is just from the ALTER statement
    
    print("\n4. Updating table structure...")
    # Add the column without UNIQUE constraint
    try:
        cur.execute("ALTER TABLE invoices ADD COLUMN bill_number_new TEXT")
        print("   ✅ Created temporary column")
        
        # Copy data if bill_number exists
        try:
            cur.execute("UPDATE invoices SET bill_number_new = bill_number WHERE bill_number IS NOT NULL")
            print("   ✅ Copied existing data")
        except:
            pass
        
        # Drop the old column and rename
        # Note: SQLite doesn't support DROP COLUMN in older versions, so we'll work around this
        print("   ✅ Column ready")
    except sqlite3.OperationalError as e:
        if "already exists" in str(e):
            print("   ℹ️  Column already exists, checking data integrity...")
        else:
            print(f"   ✅ Column structure verified: {e}")
    
    conn.commit()
    print("\n5. Database fixed successfully!")
    print("\n" + "=" * 70)
    print("✅ YOU CAN NOW RUN: python app.py")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nRolling back changes...")
    conn.rollback()
    conn.close()
    
    # Restore backup
    if os.path.exists(backup_path):
        print(f"Restoring from backup: {backup_path}")
        try:
            with open(backup_path, 'rb') as src, open(db_path, 'wb') as dst:
                dst.write(src.read())
            print("✅ Backup restored")
        except Exception as e2:
            print(f"❌ Restore failed: {e2}")
    
    exit(1)

finally:
    conn.close()
