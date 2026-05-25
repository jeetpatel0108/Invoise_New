# 🚀 Startup & Project Structure Guide

## Quick Start (One Command)

```bash
python run_all.py
```

This will:
1. Clean up unnecessary files
2. Run full test suite
3. Start the application

---

## Manual Steps

### Step 1: Install Dependencies
```bash
pip install flask flask-login reportlab qrcode[pil]
```

### Step 2: Run Tests (Optional)
```bash
python run_all_tests.py
```

### Step 3: Start Application
```bash
python app.py
```

**Access**: http://localhost:5000

---

## Project Structure

```
📦 shree-gopal-traders/
│
├── 🐍 Core Application
│   ├── app.py                    Main Flask application
│   ├── .env                      Configuration (API keys, etc.)
│   └── invoice.db                SQLite database
│
├── 📁 static/                    Frontend assets
│   ├── style.css                 Base styles
│   ├── themes.css                Theme styles
│   └── forms.js                  Form interactions
│
├── 📁 templates/                 HTML templates
│   ├── login.html                Login page
│   ├── register.html             Registration page
│   ├── index.html                Dashboard
│   ├── create.html               Create invoice form
│   ├── invoices.html             Invoice list
│   ├── unpaid_bills.html         Unpaid bills search
│   ├── success.html              Creation success page
│   ├── welcome.html              Welcome page
│   └── forgot_password.html      Password recovery
│
├── 📁 modules/                   Python modules (optional)
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── routes.py
│
├── 📁 generated_pdfs/            Invoice PDFs (auto-created)
│
├── 🧪 Testing
│   ├── run_all_tests.py          Complete test suite
│   └── run_all.py                All-in-one startup script
│
├── 🧹 Utilities
│   ├── cleanup_and_organize.py   Clean up files
│
└── 📚 Documentation
    ├── README.md
    ├── STARTUP_GUIDE.md
    ├── PAYMENT_SYSTEM_README.md
    ├── PAYMENT_FEATURES_COMPLETE.md
    ├── QUICK_START_PAYMENT_FEATURES.md
    ├── PAYMENT_SYSTEM_IMPLEMENTATION.md
    ├── PAYMENT_IMPLEMENTATION_CHECKLIST.md
    └── PAYMENT_IMPLEMENTATION_SUMMARY.md
```

---

## Key Files

### app.py
**Main application file**
- Flask routes
- Database logic
- PDF generation
- QR code generation
- Payment features

### Database (invoice.db)
**SQLite database with tables:**
- `users` - User accounts
- `invoices` - Invoice records
- `items` - Line items

### Templates
**All HTML templates located in `templates/` folder**
- Responsive design
- Payment mode selection
- Dynamic forms

### Static Files
**CSS and JavaScript in `static/` folder**
- `style.css` - Base styles
- `themes.css` - Theme colors
- `forms.js` - Form behaviors

---

## Features

### ✅ User Management
- Register new account
- Login/logout
- Forgot password with OTP
- Account settings

### ✅ Invoice Management
- Create invoices with items
- Download as PDF
- View invoice history
- Track invoice status

### ✅ Payment Tracking
- Select payment mode (CASH/ONLINE)
- Add payment reference
- QR code generation
- Payment status tracking
- Dashboard statistics
- Search unpaid bills

---

## Testing

### Run All Tests
```bash
python run_all_tests.py
```

### Individual Tests
Each test can be run independently:
- Imports verification
- Database connectivity
- Function testing
- Flask app routes
- Payment features
- Template files
- Static files

---

## Cleanup

### Remove Unnecessary Files
```bash
python cleanup_and_organize.py
```

Removes:
- Temporary files
- __pycache__ directories
- Duplicate documentation
- Old/unused files

---

## Troubleshooting

### Issue: "No module named qrcode"
```bash
pip install qrcode[pil]
```

### Issue: Database locked
- Close application
- Restart with: `python app.py`

### Issue: Port 5000 already in use
- Kill process on port 5000
- Or modify `app.run(port=5000)` in app.py

### Issue: Import errors
```bash
pip install -r requirements.txt
# or manually:
pip install flask flask-login reportlab qrcode[pil]
```

---

## File Organization

### Before Cleanup
- Many temporary files
- Duplicate documentation
- __pycache__ directories
- Scattered temp code

### After Cleanup
```
✓ Clean structure
✓ Organized folders
✓ Minimal documentation (essentials only)
✓ All code in proper locations
✓ Ready for deployment
```

---

## Environment Setup

### .env File
```
FLASK_ENV=development
DATABASE=invoice.db
SECRET_KEY=your_secret_key_here
```

---

## Running Steps

### Step 1: First Time Setup
```bash
pip install flask flask-login reportlab qrcode[pil]
python cleanup_and_organize.py
python run_all_tests.py
```

### Step 2: Regular Startup
```bash
# Option A: All-in-one
python run_all.py

# Option B: Direct
python app.py
```

### Step 3: Access Application
- Open browser: http://localhost:5000
- Default URL: http://127.0.0.1:5000

---

## Deployment

### Organize for Production
1. Clean up files: `python cleanup_and_organize.py`
2. Run tests: `python run_all_tests.py`
3. Verify structure
4. Deploy app.py

### Production Checklist
- [ ] All tests passing
- [ ] Database backed up
- [ ] Static files in place
- [ ] Templates verified
- [ ] Environment variables set
- [ ] Port configured
- [ ] SSL ready (optional)

---

## Support

### Get Help
1. Check documentation files
2. Review test output
3. Check app.py comments
4. View test_payment_features.py for examples

### Documentation Files
- `STARTUP_GUIDE.md` - This file
- `PAYMENT_SYSTEM_README.md` - Payment features
- `QUICK_START_PAYMENT_FEATURES.md` - Quick usage
- `PAYMENT_FEATURES_COMPLETE.md` - Technical details
- `README.md` - Project overview

---

## Quick Commands Reference

```bash
# Install dependencies
pip install flask flask-login reportlab qrcode[pil]

# Clean up project
python cleanup_and_organize.py

# Run tests
python run_all_tests.py

# Start app (full process)
python run_all.py

# Start app (direct)
python app.py

# Access application
# http://localhost:5000
```

---

## Project Status

✅ **Code**: Organized and clean  
✅ **Tests**: Full test suite available  
✅ **Documentation**: Comprehensive  
✅ **Features**: Payment system complete  
✅ **Ready**: For production deployment  

---

**Last Updated**: 2025-05-22  
**Version**: 2.0  
**Status**: Production Ready ✅
