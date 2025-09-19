# Flask E‑Commerce Monolith (MySQL)

A slightly large, cleanly-structured Flask application for an E‑Commerce store.

## Features
- Monolith structure with Blueprints (auth, shop, cart, orders, api)
- MySQL via SQLAlchemy (pymysql)
- User auth (register/login/logout), password hashing (bcrypt)
- Products, categories, coupons
- Cart and checkout with inventory & pricing logic (discounts, tax, shipping)
- Orders with order items
- Inventory movements (+/−) and low-stock guard
- REST APIs (`/api/v1/...`) alongside server-rendered HTML (Bootstrap 5)
- Admin via Flask‑Admin
- CSRF protection (Flask‑WTF)
- Config via `.env`
- Basic unit tests (pytest) for pricing, inventory, checkout flows

## Quickstart

1) **Create and fill `.env`** (see `.env.example`).

2) **Create DB** in MySQL:
```sql
CREATE DATABASE flask_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3) **Install**
```bash
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4) **Init DB**
```bash
flask db upgrade  # creates tables (uses Flask-Migrate autogenerate)
python -m app.seed  # optional: seed demo data
```

5) **Run**
```bash
flask --app run.py --debug run
```

Visit: http://127.0.0.1:5000

Admin at `/admin` (create a user, then mark it admin in DB or via seed).

## Tests
```bash
pytest -q
```

## Notes
- For production, configure `SECRET_KEY`, `DATABASE_URL`, and proper MySQL user perms.
- This is a template; tailor security, payments, and error handling for your needs.
