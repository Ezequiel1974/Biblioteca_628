# Biblioteca Digital 628

## Overview

This repository contains a simple Python desktop application for managing a digital library with CRUD operations for books, users, loans, categories, and related catalog data.

The UI is built with `PySide6`, and the backend uses `mysql-connector-python` to connect to a MySQL database.

## Project Structure

- `Python Backend/`
  - `ui.py` — main PySide6 application and user interface
  - `crud.py` — database access layer and CRUD helper classes
- `SQL Scripts/`
  - `20260425InitialCreation.sql` — database creation and initial schema
  - `InitialCreation_SQLServer.sql` — SQL Server version of the schema
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.11+ (recommended)
- MySQL server running locally or accessible from the app
- The Python packages listed in `requirements.txt`

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create the database schema in MySQL by running the SQL script in `SQL Scripts/20260425InitialCreation.sql`.

4. Update database connection settings in `Python Backend/crud.py` if needed:

   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'MySql!186932',
       'database': 'BibliotecaDigital628'
   }
   ```

## Run

From the repository root with the virtual environment activated:

```powershell
python "Python Backend\ui.py"
```

## Notes

- The app launches a GUI for library management.
- Make sure the MySQL database exists and the credentials in `crud.py` match your environment.
- Use the SQL scripts to create or migrate the database schema.
