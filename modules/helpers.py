import re
import hashlib
import secrets
import time
import os
from modules.database import db_conn

OTP_EXPIRY_SECONDS = 600
OTP_MAX_ATTEMPTS = 5


def normalize_phone(raw):
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) == 10:
        digits = "91" + digits
    return digits


def mask_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) >= 4:
        return "******" + digits[-4:]
    if len(digits) >= 3:
        return "*******" + digits[-3:]
    return "********"


def validate_register_data(form):
    username = form.get("u", "").strip()
    password = form.get("p", "")
    shop = form.get("sn", "").strip()
    owner = form.get("on", form.get("owner_name", "")).strip()
    address = form.get("a", form.get("addr", "")).strip()
    city = form.get("c", "").strip()
    phone_raw = form.get("ph", "").strip()
    gst = form.get("g", form.get("gst", "")).strip()

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return None, "Username: 3–20 characters, letters, numbers, underscore only."
    if len(password) < 6:
        return None, "Password: minimum 6 characters required."
    if not shop or len(shop) < 2:
        return None, "Shop name is required."
    if re.search(r"[^a-zA-Z0-9\s.\-&]", shop):
        return None, "Shop name: no special symbols (letters and numbers only)."
    if not re.match(r"^[a-zA-Z\s]{2,50}$", owner):
        return None, "Owner name: letters only, no numbers."
    if len(address) < 5:
        return None, "Address: please enter full address."
    if not re.match(r"^[a-zA-Z\s]{2,50}$", city):
        return None, "City: letters only, no numbers."
    phone = normalize_phone(phone_raw)
    if len(phone) < 12 or len(phone) > 12:
        return None, "Phone: enter 10-digit mobile number (numbers only, no letters)."
    if gst and not re.match(
        r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$", gst.upper()
    ):
        return None, "GST: invalid format (optional field)."

    return {
        "username": username,
        "password": password,
        "shop_name": shop,
        "owner_name": owner,
        "address": ", ".join(p for p in (address, city) if p),
        "phone": phone,
        "gst": gst.upper() if gst else "",
    }, None


def send_otp_sms(phone, otp):
    """Send OTP via Fast2SMS if configured; else demo log (see README)."""
    message = f"Shree Gopal Traders: Your password reset OTP is {otp}. Valid 10 min."
    api_key = os.environ.get("FAST2SMS_API_KEY", "").strip()
    if api_key:
        try:
            import urllib.parse
            import urllib.request

            data = urllib.parse.urlencode(
                {
                    "route": "q",
                    "message": message,
                    "numbers": phone,
                }
            ).encode()
            req = urllib.request.Request(
                "https://www.fast2sms.com/dev/bulkV2",
                data=data,
                headers={"authorization": api_key},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status == 200
        except Exception:
            return False

    print(f"[OTP SMS demo] To {phone}: {otp}")
    return True


def store_otp(username, otp):
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    expires = int(time.time()) + OTP_EXPIRY_SECONDS
    conn = db_conn()
    conn.execute(
        """INSERT INTO password_otp (username, otp_hash, expires_at, attempts)
           VALUES (?, ?, ?, 0)
           ON CONFLICT(username) DO UPDATE SET
             otp_hash=excluded.otp_hash,
             expires_at=excluded.expires_at,
             attempts=0""",
        (username, otp_hash, expires),
    )
    conn.commit()
    conn.close()


def verify_otp(username, otp):
    conn = db_conn()
    row = conn.execute(
        "SELECT otp_hash, expires_at, attempts FROM password_otp WHERE username=?",
        (username,),
    ).fetchone()
    if not row:
        conn.close()
        return False, "OTP not found. Request a new OTP."
    otp_hash, expires_at, attempts = row
    if attempts >= OTP_MAX_ATTEMPTS:
        conn.close()
        return False, "Too many wrong attempts. Request a new OTP."
    if int(time.time()) > expires_at:
        conn.close()
        return False, "OTP expired. Request a new OTP."
    given = hashlib.sha256(otp.encode()).hexdigest()
    if not secrets.compare_digest(given, otp_hash):
        conn.execute(
            "UPDATE password_otp SET attempts=attempts+1 WHERE username=?",
            (username,),
        )
        conn.commit()
        conn.close()
        return False, "Invalid OTP. Please try again."
    conn.execute("DELETE FROM password_otp WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return True, None

