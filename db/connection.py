import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "invoice.db"


def db_conn():
    return sqlite3.connect(str(DB_FILE), timeout=30)


def _simple_bill_number(seq):
    return f"{int(seq):02d}"


def normalize_bill_numbers(conn):
    cur = conn.cursor()
    user_ids = [
        row[0]
        for row in cur.execute(
            "SELECT DISTINCT user_id FROM invoices WHERE user_id IS NOT NULL ORDER BY user_id"
        ).fetchall()
    ]
    for user_id in user_ids:
        rows = cur.execute(
            "SELECT id, bill_number FROM invoices WHERE user_id=? ORDER BY id",
            (user_id,),
        ).fetchall()
        for seq, (invoice_id, bill_number) in enumerate(rows, start=1):
            simple = _simple_bill_number(seq)
            if bill_number != simple:
                cur.execute(
                    "UPDATE invoices SET bill_number=? WHERE id=?",
                    (simple, invoice_id),
                )


def init_db():
    conn = db_conn()
    cur = conn.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            shop_name TEXT,
            owner_name TEXT,
            phone TEXT,
            gst TEXT,
            address TEXT)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS invoices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer TEXT,
            phone TEXT,
            customer_address TEXT,
            date TEXT,
            bill_number TEXT UNIQUE,
            payment_mode TEXT DEFAULT 'CASH',
            payment_status TEXT DEFAULT 'UNPAID',
            payment_reference TEXT,
            payment_date TEXT)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            name TEXT,
            qty INTEGER,
            price REAL)'''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS password_otp(
            username TEXT PRIMARY KEY,
            otp_hash TEXT NOT NULL,
            expires_at INTEGER NOT NULL,
            attempts INTEGER DEFAULT 0)'''
    )

    invoice_cols = {row[1] for row in cur.execute("PRAGMA table_info(invoices)").fetchall()}
    if "customer" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN customer TEXT")
    if "phone" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN phone TEXT")
    if "customer_address" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN customer_address TEXT")
    if "date" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN date TEXT")
    if "bill_number" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN bill_number TEXT")
    if "payment_mode" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN payment_mode TEXT DEFAULT 'CASH'")
    if "payment_status" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN payment_status TEXT DEFAULT 'UNPAID'")
    if "payment_reference" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN payment_reference TEXT")
    if "payment_date" not in invoice_cols:
        cur.execute("ALTER TABLE invoices ADD COLUMN payment_date TEXT")

    cur.execute("UPDATE invoices SET payment_status='UNPAID' WHERE payment_status IS NULL OR payment_status=''")
    cur.execute("UPDATE invoices SET payment_mode='CASH' WHERE payment_mode IS NULL OR payment_mode=''")

    user_cols = {row[1] for row in cur.execute("PRAGMA table_info(users)").fetchall()}
    if "shop_name" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN shop_name TEXT")
    if "email" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
    if "owner_name" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN owner_name TEXT")
    if "phone" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    if "gst" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN gst TEXT")
    if "address" not in user_cols:
        cur.execute("ALTER TABLE users ADD COLUMN address TEXT")

    cur.execute("UPDATE users SET email=NULL WHERE email='' OR email IS NULL")
    normalize_bill_numbers(conn)
    conn.commit()
    conn.close()


def generate_bill_number(user_id, date_str):
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        user_id = 0

    conn = db_conn()
    cur = conn.cursor()
    result = cur.execute(
        """SELECT MAX(CAST(bill_number AS INTEGER))
           FROM invoices
           WHERE user_id=? AND bill_number GLOB '[0-9]*'""",
        (user_id,),
    ).fetchone()
    count = int(result[0] or 0) + 1
    conn.close()

    return _simple_bill_number(count)
