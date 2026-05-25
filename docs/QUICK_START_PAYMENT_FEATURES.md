# 🚀 Quick Start - Payment Features Guide

## Installation (One-time setup)

### Step 1: Install QR Code Library
```bash
pip install qrcode[pil]
```

### Step 2: Start the Application
```bash
python app.py
```

The database will auto-update with payment columns on startup.

---

## 📝 Creating an Invoice with Payment Info

### Option A: CASH Payment
1. Go to **Create Invoice**
2. Fill in customer details
3. **Select Payment Mode: 💵 CASH**
4. Add items
5. Click **Generate Invoice**
6. ✅ Invoice created (no QR code)

### Option B: ONLINE Payment
1. Go to **Create Invoice**
2. Fill in customer details
3. **Select Payment Mode: 💳 ONLINE**
4. **Payment Reference field appears** ← Enter transaction ID (optional)
   - Example: `TXN-123456789`
   - Example: `UPI-REF-12345`
   - Leave blank if not available
5. Add items
6. Click **Generate Invoice**
7. ✅ Invoice created with reference stored

---

## 📥 Download Invoice PDF

### CASH Invoice PDF Shows:
```
Bill No: INV-20250521-001-0001
Date: 2025-05-21
Payment Mode: CASH
Status: UNPAID

[Items and totals]

Footer: "Thank you for your business!" | "Authorized Signatory"
```

### ONLINE Invoice PDF Shows:
```
Bill No: INV-20250521-001-0001
Date: 2025-05-21
Payment Mode: ONLINE
Status: UNPAID
Reference: TXN-123456789 (blue background)

[Items and totals]

Footer: "Thank you!" | [QR Code 80x80]
```

**QR Code contains**: Bill total amount (e.g., "1000.00")

---

## 💳 Track Payments on Dashboard

### Payment Statistics Widget
Shows:
- **Paid Bills**: Count and total amount
- **Unpaid Bills**: Count and total amount
- **Paid %**: Percentage of paid invoices
- **Outstanding**: Total unpaid amount

### Quick Actions
- Click **"💳 Payment Tracking"** to search unpaid bills

---

## 🔍 Search Unpaid Invoices

### Step 1: Go to Payment Tracking
Click **"💳 Payment Tracking"** on dashboard

### Step 2: Use Filters

**Filter by Status**:
- PAID - shows only paid invoices
- UNPAID - shows only unpaid invoices

**Filter by Customer Name**:
- Type customer name to find their invoices

**Filter by Bill Number**:
- Type or paste full bill number (e.g., INV-20250521-001-0001)

**Filter by Date Range**:
- Select From Date and To Date
- Shows invoices in that range

### Step 3: View Results
- See bill number, customer, amount, date
- Shows payment mode (CASH/ONLINE)
- Shows payment status (PAID/UNPAID)
- View total unpaid amount at bottom

---

## ✅ Mark Invoice as Paid

### Method 1: From Payment Tracking Page
1. Go to **"💳 Payment Tracking"**
2. Find the invoice
3. Click **"Mark as Paid"** button
4. ✅ Status changes to PAID

### Method 2: From Invoice List
1. Go to **View Invoices**
2. Find the invoice
3. Status badge shows current state
4. (More detailed mark-as-paid coming soon)

### Undo Payment
1. Go to **"💳 Payment Tracking"**
2. Filter by status: PAID
3. Click **"Mark as Unpaid"** to revert
4. ✅ Status changes back to UNPAID

---

## 📊 Common Tasks

### Task: Create CASH Invoice Without QR
1. Select Payment Mode: CASH ✓
2. Payment Reference field stays hidden ✓
3. Download PDF - no QR code ✓

### Task: Create ONLINE Invoice with QR
1. Select Payment Mode: ONLINE ✓
2. Payment Reference field appears ✓
3. Enter reference (optional) ✓
4. Download PDF - shows QR code ✓

### Task: Find All Unpaid Invoices
1. Go to Payment Tracking ✓
2. Filter: Status = UNPAID ✓
3. View list with totals ✓

### Task: Find Unpaid Bills for Specific Customer
1. Go to Payment Tracking ✓
2. Filter: Customer Name = {name} ✓
3. Also select: Status = UNPAID ✓
4. View their unpaid invoices ✓

### Task: Update Invoice Payment Status
1. Go to Payment Tracking ✓
2. Find invoice ✓
3. Click Mark as Paid/Unpaid ✓
4. See status update immediately ✓

### Task: Check Dashboard Statistics
1. Go to Home/Dashboard ✓
2. Scroll to Payment Statistics ✓
3. See paid/unpaid summary ✓
4. See total amounts and percentage ✓

---

## 🎨 UI Changes You'll See

### Invoice Creation Form
```
Customer Name: _______
Customer Phone: _______
Customer Address: _______

Authorized Signatory: _______

Payment Mode: [Select ▼]
  - 💵 CASH
  - 💳 ONLINE

[Payment Reference field appears only for ONLINE]

Items:
  Item Name | Qty | Price
  ...

[+ Add More Items] [Generate Invoice]
```

### Dashboard Payment Section
```
📊 Payment Statistics
┌─────────────────────────┐
│ Paid Bills: 10 (₹30,000)  │
│ Unpaid Bills: 5 (₹15,000) │
│ Paid Percentage: 66.7%    │
│ Outstanding: ₹15,000      │
│                            │
│ [💳 Payment Tracking]      │
└─────────────────────────┘
```

### Invoice List
```
Bill No          | Customer    | Status    | Mode
INV-20250521-001 | John        | ✅ PAID   | CASH
INV-20250521-002 | Sarah       | ⏳ UNPAID | ONLINE
INV-20250521-003 | Mike        | ✅ PAID   | CASH
```

---

## ⚠️ Important Notes

1. **QR Code**: Contains only the bill amount
   - Not a payment link
   - For verification purposes
   - Can be scanned to confirm amount

2. **Payment Reference**: User-entered
   - Keep for your records
   - Can be any transaction ID or reference
   - Optional field

3. **Payment Status**: Manual tracking
   - You mark when payment is received
   - Updates dashboard statistics
   - Can be toggled if needed

4. **Default Values**:
   - New invoices default to: CASH, UNPAID
   - Old invoices auto-updated to same defaults
   - No data loss

---

## 🔧 Troubleshooting

### Issue: Payment Reference field not appearing
**Solution**: Make sure you selected ONLINE payment mode

### Issue: QR code not showing in PDF
**Solution**: Check that:
1. Payment mode is ONLINE (not CASH)
2. qrcode library is installed (`pip install qrcode[pil]`)

### Issue: Dashboard statistics not updating
**Solution**: 
1. Refresh the page
2. Clear browser cache
3. Restart application

### Issue: Can't find unpaid invoice
**Solution**: 
1. Check payment status filter
2. Try removing date filter
3. Search by bill number

---

## 📞 Quick Reference

### Commands to Install & Run
```bash
# Install QR library
pip install qrcode[pil]

# Start application
python app.py

# Test payment features
python test_payment_features.py
```

### Navigation
- **Create Invoice**: Home → Create Invoice
- **View Invoices**: Home → View Invoices
- **Payment Tracking**: Dashboard → "💳 Payment Tracking" Button
- **Download Invoice**: Invoice List → Download Button

### Features
- **Payment Mode**: Select during invoice creation
- **Payment Reference**: Enter for ONLINE invoices
- **QR Code**: Auto-generated, appears in PDF for ONLINE only
- **Dashboard Stats**: Shows on home page
- **Search Unpaid**: Use Payment Tracking page

---

## ✨ Summary

**All Payment Features Ready to Use:**
- ✅ CASH/ONLINE payment modes
- ✅ Payment reference tracking
- ✅ QR code generation
- ✅ Dashboard statistics
- ✅ Unpaid bills search
- ✅ Payment status management

**Start creating invoices with payment tracking today!**

---

For detailed technical information, see:
- `PAYMENT_FEATURES_COMPLETE.md` - Technical details
- `PAYMENT_SYSTEM_README.md` - Full documentation
- `PAYMENT_IMPLEMENTATION_CHECKLIST.md` - Implementation status
