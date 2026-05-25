# Invoice Management System - Project Structure

## Overview
The project has been reorganized into a modular structure for better maintainability and scalability.

## Directory Structure

```
shree_gopal_traders/
├── app.py                 # Main application entry point (run this file)
├── invoice.db             # SQLite database (auto-created)
├── PROJECT_STRUCTURE.md   # This file
│
├── modules/               # All application logic (MODULAR)
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database initialization and utilities
│   ├── models.py          # User model and database operations
│   └── routes.py          # All Flask routes
│
├── templates/             # HTML templates
│   ├── index.html         # Dashboard
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── create.html        # Create invoice page
│   ├── invoices.html      # Invoice list page
│   ├── success.html       # Success page
│   └── welcome.html       # Welcome page
│
├── static/                # Static files
│   └── style.css          # Stylesheet
│
└── generated_pdfs/        # Generated PDF invoices (auto-created)
```

## Module Descriptions

### 1. **app.py** (Entry Point)
The main application file. This is the file you run to start the application.

```bash
python app.py
```

### 2. **modules/** (Application Logic)
Contains all business logic separated by concern.

## License
Private use - Shree Gopal Traders
