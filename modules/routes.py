import re
import secrets
import os
from pathlib import Path

from flask import render_template, request, redirect, url_for, send_file, session
from flask_login import login_user, login_required, logout_user, current_user
from modules.helpers import (
    generate_qr_code,
    normalize_phone,
    mask_phone,
    validate_register_data,
    send_otp_sms,
    store_otp,
    verify_otp,
)
from modules.models import User
from modules.database import db_conn, generate_bill_number
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

PDF_FOLDER = Path(__file__).resolve().parent.parent / "generated_pdfs"
PDF_FOLDER.mkdir(parents=True, exist_ok=True)


def format_invoice_date(value):
    raw = str(value or "").strip()
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if match:
        year, month, day = match.groups()
        return f"{day}/{month}/{year}"
    return raw or "-"


def init_routes(app):

    @app.route("/")
    def home():
        if not current_user.is_authenticated:
            return redirect(url_for("login"))

        conn = db_conn()
        owner = conn.execute(
            "SELECT owner_name, shop_name FROM users WHERE id=?",
            (current_user.id,),
        ).fetchone()

        daily_stats = conn.execute(
            """SELECT COUNT(DISTINCT invoices.id), COALESCE(SUM(items.qty * items.price), 0)
               FROM invoices
               LEFT JOIN items ON items.invoice_id = invoices.id
               WHERE invoices.user_id = ?
               AND invoices.date = date('now', 'localtime')""",
            (current_user.id,),
        ).fetchone()

        overall_stats = conn.execute(
            """SELECT COUNT(DISTINCT invoices.id), COALESCE(SUM(items.qty * items.price), 0)
               FROM invoices
               LEFT JOIN items ON items.invoice_id = invoices.id
               WHERE invoices.user_id = ?""",
            (current_user.id,),
        ).fetchone()

        paid_stats = conn.execute(
            """SELECT COUNT(DISTINCT invoices.id), COALESCE(SUM(items.qty * items.price), 0)
               FROM invoices
               LEFT JOIN items ON items.invoice_id = invoices.id
               WHERE invoices.user_id = ? AND invoices.payment_status = 'PAID'""",
            (current_user.id,),
        ).fetchone()

        unpaid_stats = conn.execute(
            """SELECT COUNT(DISTINCT invoices.id), COALESCE(SUM(items.qty * items.price), 0)
               FROM invoices
               LEFT JOIN items ON items.invoice_id = invoices.id
               WHERE invoices.user_id = ? AND invoices.payment_status = 'UNPAID'""",
            (current_user.id,),
        ).fetchone()

        recent_bills = conn.execute(
            """SELECT invoices.id, invoices.customer, invoices.date,
                      COALESCE(SUM(items.qty * items.price), 0) AS total,
                      invoices.bill_number, invoices.payment_status, invoices.payment_mode
               FROM invoices
               LEFT JOIN items ON items.invoice_id = invoices.id
               WHERE invoices.user_id = ?
               GROUP BY invoices.id, invoices.customer, invoices.date, invoices.bill_number, invoices.payment_status, invoices.payment_mode
               ORDER BY invoices.id DESC
               LIMIT 5""",
            (current_user.id,),
        ).fetchall()
        conn.close()

        return render_template(
            "index.html",
            owner_name=(owner[0] if owner and owner[0] else "Owner"),
            shop_name=(owner[1] if owner and owner[1] else "My Shop"),
            daily_bill_count=(daily_stats[0] if daily_stats else 0),
            daily_bill_amount=(daily_stats[1] if daily_stats else 0),
            total_bill_count=(overall_stats[0] if overall_stats else 0),
            total_bill_amount=(overall_stats[1] if overall_stats else 0),
            paid_bill_count=(paid_stats[0] if paid_stats else 0),
            paid_bill_amount=(paid_stats[1] if paid_stats else 0),
            unpaid_bill_count=(unpaid_stats[0] if unpaid_stats else 0),
            unpaid_bill_amount=(unpaid_stats[1] if unpaid_stats else 0),
            recent_bills=recent_bills,
        )

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            data, err = validate_register_data(request.form)
            if err:
                return render_template("register.html", error=err)
            try:
                conn = db_conn()
                conn.execute(
                    """INSERT INTO users
                       (username, email, password, shop_name, owner_name, phone, gst, address)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        data["username"],
                        None,
                        data["password"],
                        data["shop_name"],
                        data["owner_name"],
                        data["phone"],
                        data["gst"],
                        data["address"],
                    ),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            except Exception:
                return render_template(
                    "register.html",
                    error="Username already taken. Choose another or login.",
                )
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            conn = db_conn()
            user = conn.execute(
                "SELECT id FROM users WHERE username=? AND password=?",
                (request.form["u"].strip(), request.form["p"]),
            ).fetchone()
            conn.close()
            if user:
                login_user(User(str(user[0])))
                return redirect("/")
            return render_template("login.html", error="Invalid username or password.")
        return render_template("login.html")

    @app.route("/forgot-password")
    def forgot_password():
        return render_template("forgot_password.html", step="username")

    @app.route("/forgot-password/send", methods=["GET", "POST"])
    def forgot_password_send():
        username = (request.form.get("u") or request.args.get("u") or "").strip()
        if request.method == "GET" and request.args.get("resend") and username:
            pass
        elif request.method != "POST":
            return redirect(url_for("forgot_password"))

        if not username:
            return render_template(
                "forgot_password.html",
                step="username",
                error="Enter your username.",
            )

        conn = db_conn()
        row = conn.execute("SELECT phone FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        if not row or not row[0]:
            return render_template(
                "forgot_password.html",
                step="username",
                error="Username not found or no phone on file. Contact support.",
            )

        phone = normalize_phone(row[0])
        otp = f"{secrets.randbelow(1000000):06d}"
        if not send_otp_sms(phone, otp):
            return render_template(
                "forgot_password.html",
                step="username",
                error="Could not send SMS. Set FAST2SMS_API_KEY or check server logs (demo mode).",
            )

        store_otp(username, otp)
        phone_mask = mask_phone(phone)
        session["reset_username"] = username
        session["reset_phone_mask"] = phone_mask
        session.pop("reset_verified", None)
        demo_otp = otp if not os.environ.get("FAST2SMS_API_KEY", "").strip() else None
        return render_template(
            "forgot_password.html",
            step="otp",
            username=username,
            phone_mask=phone_mask,
            demo_otp=demo_otp,
            show_otp_popup=True,
        )

    @app.route("/forgot-password/verify", methods=["POST"])
    def forgot_password_verify():
        username = session.get("reset_username") or request.form.get("u", "").strip()
        otp = re.sub(r"\D", "", request.form.get("otp", ""))
        if not username:
            return render_template(
                "forgot_password.html",
                step="username",
                error="OTP session expired. Please request a new OTP.",
            )
        if not username or len(otp) != 6:
            return render_template(
                "forgot_password.html",
                step="otp",
                username=username,
                error="Enter 6-digit OTP (numbers only).",
            )
        ok, err = verify_otp(username, otp)
        if not ok:
            return render_template(
                "forgot_password.html",
                step="otp",
                username=username,
                error=err,
            )
        session["reset_verified"] = username
        return render_template(
            "forgot_password.html",
            step="reset",
            username=username,
            info="OTP verified. Set your new password.",
        )

    @app.route("/forgot-password/reset", methods=["POST"])
    def forgot_password_reset():
        username = session.get("reset_verified") or request.form.get("u", "").strip()
        if session.get("reset_verified") != username:
            return render_template(
                "forgot_password.html",
                step="username",
                error="Reset session expired. Please request a new OTP.",
            )

        p1 = request.form.get("p", "")
        p2 = request.form.get("p2", "")
        if len(p1) < 6:
            return render_template(
                "forgot_password.html",
                step="reset",
                username=username,
                error="Password must be at least 6 characters.",
            )
        if p1 != p2:
            return render_template(
                "forgot_password.html",
                step="reset",
                username=username,
                error="Passwords do not match.",
            )

        conn = db_conn()
        conn.execute("UPDATE users SET password=? WHERE username=?", (p1, username))
        conn.commit()
        conn.close()
        session.pop("reset_verified", None)
        session.pop("reset_username", None)
        return render_template(
            "login.html",
            info="Password reset successful. Please login.",
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/login")

    @app.route("/create", methods=["GET", "POST"])
    @login_required
    def create():
        if request.method == "POST":
            conn = db_conn()
            cur = conn.cursor()

            cus_name = request.form.get("cus_n") or request.form.get("cus", "")
            cus_phone = request.form.get("cus_ph") or request.form.get("ph", "")
            cus_addr = request.form.get("cus_addr") or request.form.get("address", "")
            invoice_date = request.form["date"]
            payment_mode = request.form.get("payment_mode", "CASH").upper()
            if payment_mode not in ["CASH", "ONLINE"]:
                payment_mode = "CASH"

            bill_number = generate_bill_number(current_user.id, invoice_date)
            payment_reference = ""
            if payment_mode == "ONLINE":
                payment_reference = request.form.get("payment_reference", "").strip()

            cur.execute(
                """INSERT INTO invoices
                   (user_id, customer, phone, customer_address, date, bill_number, payment_mode, payment_status, payment_reference)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    current_user.id,
                    cus_name,
                    cus_phone,
                    cus_addr,
                    invoice_date,
                    bill_number,
                    payment_mode,
                    "UNPAID",
                    payment_reference,
                ),
            )
            inv_id = cur.lastrowid

            names = request.form.getlist("item_n[]") or request.form.getlist("name[]")
            qtys = request.form.getlist("item_q[]") or request.form.getlist("qty[]")
            prices = request.form.getlist("item_p[]") or request.form.getlist("price[]")

            for n, q, p in zip(names, qtys, prices):
                name = (n or "").strip()
                if not name:
                    continue
                try:
                    qty = int(q)
                    price = float(p)
                except (TypeError, ValueError):
                    continue
                cur.execute(
                    "INSERT INTO items (invoice_id, name, qty, price) VALUES (?,?,?,?)",
                    (inv_id, name, qty, price),
                )

            conn.commit()
            conn.close()
            whatsapp_url = f"https://wa.me/{cus_phone}?text=Hello%20{cus_name},%20your%20invoice%20#{bill_number}%20is%20ready."
            return render_template("success.html", inv_id=inv_id, bill_number=bill_number, whatsapp_url=whatsapp_url)

        return render_template("create.html")

    @app.route("/download/<int:id>")
    @login_required
    def download(id):
        conn = db_conn()
        inv = conn.execute(
            """SELECT id, user_id, customer, phone, customer_address, date, bill_number, payment_mode, payment_status, payment_reference
               FROM invoices
               WHERE id=? AND user_id=?""",
            (id, current_user.id),
        ).fetchone()
        if not inv:
            conn.close()
            return redirect(url_for("invoices"))

        shop = conn.execute(
            "SELECT shop_name, owner_name, phone, gst, address FROM users WHERE id=?",
            (inv[1],),
        ).fetchone()
        items = conn.execute("SELECT name,qty,price FROM items WHERE invoice_id=?", (id,)).fetchall()
        conn.close()

        file = str(PDF_FOLDER / f"invoice_{id}.pdf")
        doc = SimpleDocTemplate(file, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()
        content_width = doc.width

        text_color = colors.black
        print_line = colors.black
        header_bg = colors.HexColor('#E8F5E9')
        section_bg = colors.HexColor('#F7FBF9')
        shop_name = (shop[0] or "SHOP").upper()
        owner_name = shop[1] or "-"
        shop_phone = shop[2] or "-"
        gst = (shop[3] or "").strip()
        shop_address = shop[4] or "-"
        customer_name = inv[2] or "-"
        customer_phone = inv[3] or "-"
        customer_address = inv[4] or "-"
        invoice_date = format_invoice_date(inv[5])
        bill_number = app.jinja_env.filters["short_bill"](inv[6] or id)
        payment_mode = inv[7] or "CASH"
        payment_status = inv[8] or "UNPAID"
        payment_reference = inv[9] or ""

        title_block = Table(
            [
                [Paragraph(f"{shop_name}", ParagraphStyle('Shop', fontSize=18, textColor=text_color, alignment=TA_CENTER))],
                [Paragraph("TAX INVOICE", ParagraphStyle('Title', fontSize=16, alignment=TA_CENTER))],
            ],
            colWidths=[content_width],
        )
        title_block.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), header_bg),
                ('BOX', (0, 0), (-1, -1), 1.2, print_line),
                ('LINEABOVE', (0, 1), (0, 1), 1.0, print_line),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ])
        )

        gst_line = f"GST: {gst}<br/>" if gst else ""

        info_data = [
            [
                Paragraph(
                    f"<b>Owner Information</b><br/>"
                    f"Owner: {owner_name}<br/>"
                    f"Phone: {shop_phone}<br/>"
                    f"{gst_line}"
                    f"Address: {shop_address}",
                    styles["Normal"],
                ),
                Paragraph(
                    f"<b>Customer Information</b><br/>"
                    f"Customer: {customer_name}<br/>"
                    f"Phone: {customer_phone}<br/>"
                    f"Address: {customer_address}",
                    styles["Normal"],
                ),
            ]
        ]
        half_width = content_width / 2
        info_table = Table(info_data, colWidths=[half_width, half_width])
        info_table.setStyle(
            TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, -1), section_bg),
                ('BOX', (0, 0), (-1, -1), 1.2, print_line),
                ('LINEBEFORE', (1, 0), (1, 0), 1.2, print_line),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )

        meta_rows = [
            [f"Bill No: {bill_number}", f"Date: {invoice_date}"],
            [f"Payment Mode: {payment_mode}", f"Status: {payment_status}"],
        ]
        if payment_mode == "ONLINE" and payment_reference:
            meta_rows.append([f"Reference: {payment_reference}", ""])

        meta_table = Table(meta_rows, colWidths=[half_width, half_width])
        meta_style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), header_bg),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFF3E0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), text_color),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1.0, print_line),
            ('BOX', (0, 0), (-1, -1), 1.2, print_line),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
        if len(meta_rows) > 2:
            meta_style_cmds.append(('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#E3F2FD')))
        meta_table.setStyle(TableStyle(meta_style_cmds))

        data = [["Item", "Qty", "Price", "Total"]]
        total = 0
        for n, q, p in items:
            line_total = q * p
            total += line_total
            data.append([n, str(q), f"{p:,.2f}", f"{line_total:,.2f}"])
        if not items:
            data.append(["No items added", "-", "-", "0.00"])
        data.append(["", "", "Grand Total", f"{total:,.2f}"])

        item_col_widths = [content_width * 0.5, content_width * 0.13, content_width * 0.18, content_width * 0.19]
        item_table = Table(data, colWidths=item_col_widths)
        item_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8F5E9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), text_color),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1.0, print_line),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -2), 'CENTER'),
                ('ALIGN', (2, 1), (3, -2), 'RIGHT'),
                ('ALIGN', (2, -1), (3, -1), 'RIGHT'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('FONTNAME', (2, -1), (3, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (2, -1), (3, -1), colors.HexColor('#F1F8E9')),
                ('BOX', (2, -1), (3, -1), 1.4, print_line),
                ('LINEABOVE', (0, -1), (-1, -1), 1.2, print_line),
            ])
        )

        footer_table = Table(
            [[
                Paragraph("Thank you for your business!", styles["Normal"]),
                Paragraph("Authorized Signatory", ParagraphStyle('Sig', alignment=TA_CENTER)),
            ]],
            colWidths=[content_width * 0.62, content_width * 0.38],
        )
        footer_table.setStyle(
            TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.2, print_line),
                ('LINEBEFORE', (1, 0), (1, 0), 1.2, print_line),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
        )

        frame = Table([[title_block], [meta_table], [info_table], [item_table], [footer_table]], colWidths=[content_width])
        frame.setStyle(
            TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.4, print_line),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])
        )

        story = [frame]
        doc.build(story)
        return send_file(file, as_attachment=True)

    @app.route("/invoices")
    @login_required
    def invoices():
        conn = db_conn()
        rows = conn.execute(
            """SELECT invoices.id, invoices.customer, invoices.date, invoices.bill_number, invoices.payment_status
               FROM invoices
               WHERE invoices.user_id = ?
               ORDER BY invoices.id DESC""",
            (current_user.id,),
        ).fetchall()
        shop = conn.execute("SELECT shop_name FROM users WHERE id=?", (current_user.id,)).fetchone()
        conn.close()
        shop_name = shop[0] if shop and shop[0] else "My Shop"
        safe_rows = [
            (r[0], shop_name, r[1], r[2] or f"INV-{r[0]}", r[3], r[4])
            for r in rows
        ]
        return render_template("invoices.html", invoices=safe_rows)

    @app.route("/unpaid-bills", methods=["GET", "POST"])
    @login_required
    def unpaid_bills():
        conn = db_conn()
        status_filter = request.args.get("status", "unpaid").lower()
        customer_filter = request.args.get("customer", "").strip()
        bill_filter = request.args.get("bill", "").strip()
        date_from = request.args.get("date_from", "")
        date_to = request.args.get("date_to", "")

        query = """SELECT invoices.id, invoices.bill_number, invoices.customer,
               COALESCE(SUM(items.qty * items.price), 0) AS total,
               invoices.date, invoices.payment_mode, invoices.payment_status
        FROM invoices
        LEFT JOIN items ON items.invoice_id = invoices.id
        WHERE invoices.user_id = ?"""
        params = [current_user.id]

        if status_filter == "paid":
            query += " AND invoices.payment_status = 'PAID'"
        elif status_filter == "unpaid":
            query += " AND invoices.payment_status = 'UNPAID'"
        if customer_filter:
            query += " AND invoices.customer LIKE ?"
            params.append(f"%{customer_filter}%")
        if bill_filter:
            query += " AND invoices.bill_number LIKE ?"
            params.append(f"%{bill_filter}%")
        if date_from:
            query += " AND invoices.date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND invoices.date <= ?"
            params.append(date_to)

        query += " GROUP BY invoices.id ORDER BY invoices.date DESC"
        rows = conn.execute(query, params).fetchall()

        total_unpaid = sum(r[3] for r in rows if r[6] == "UNPAID")
        total_paid = sum(r[3] for r in rows if r[6] == "PAID")
        conn.close()

        return render_template(
            "unpaid_bills.html",
            bills=rows,
            total_unpaid=total_unpaid,
            total_paid=total_paid,
            status_filter=status_filter,
            customer_filter=customer_filter,
            bill_filter=bill_filter,
            date_from=date_from,
            date_to=date_to,
        )

    @app.route("/mark-paid/<int:id>", methods=["POST"])
    @login_required
    def mark_paid_alias(id):
        return mark_paid(bill_id=id)

    @app.route("/mark-paid/<int:bill_id>", methods=["POST"])
    @login_required
    def mark_paid(bill_id):
        conn = db_conn()
        inv = conn.execute(
            "SELECT payment_status FROM invoices WHERE id=? AND user_id=?",
            (bill_id, current_user.id),
        ).fetchone()
        if not inv:
            conn.close()
            return redirect(url_for("unpaid_bills"))

        new_status = "PAID" if inv[0] != "PAID" else "UNPAID"
        conn.execute("UPDATE invoices SET payment_status=? WHERE id=?", (new_status, bill_id))
        conn.commit()
        conn.close()
        return redirect(request.referrer or url_for("unpaid_bills"))
