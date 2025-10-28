# SecureBook API (Simple Secure Example)

This is a small, self-contained FastAPI project that demonstrates secure practices:
- JWT authentication
- Role-based access control (RBAC)
- Input validation with Pydantic
- Parameterized DB access using SQLAlchemy
- Simple in-memory rate limiting (suitable for demo/testing)
- Structured JSON logging

## Run locally (recommended)
1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (example):
   ```bash
    SECRET_KEY='change_this_to_a_strong_secret'
    ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```
   On Windows (PowerShell):
   ```powershell
   $env:SECRET_KEY = 'change_this_to_a_strong_secret'
   $env:ACCESS_TOKEN_EXPIRE_MINUTES = '15'
   ```
4. Run the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open docs: http://127.0.0.1:8000/docs

## Default demo users (created on first run)
- admin / adminpass  (role: admin, writer, reader)
- writer / writerpass (role: writer, reader)
- reader / readerpass (role: reader)

## Notes
- For production use: replace SECRET_KEY, use a real database (Postgres), use HTTPS, and a proper rate limiter (Redis).
