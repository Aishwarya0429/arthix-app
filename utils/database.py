import sqlite3
import hashlib
import os
from datetime import datetime, date, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "arthix.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        email       TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL,
        role        TEXT DEFAULT 'Staff',
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS businesses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        name        TEXT NOT NULL,
        category    TEXT,
        currency    TEXT DEFAULT 'INR',
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        type        TEXT NOT NULL,
        category    TEXT,
        amount      REAL NOT NULL,
        description TEXT,
        txn_date    DATE NOT NULL,
        receipt_url TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(business_id) REFERENCES businesses(id)
    );

    CREATE TABLE IF NOT EXISTS products (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        name        TEXT NOT NULL,
        sku         TEXT,
        cost_price  REAL DEFAULT 0,
        sale_price  REAL DEFAULT 0,
        stock       INTEGER DEFAULT 0,
        low_stock_threshold INTEGER DEFAULT 10,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(business_id) REFERENCES businesses(id)
    );

    CREATE TABLE IF NOT EXISTS inventory_logs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id  INTEGER NOT NULL,
        change      INTEGER NOT NULL,
        reason      TEXT,
        logged_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );

    CREATE TABLE IF NOT EXISTS reports (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        report_type TEXT,
        file_path   TEXT,
        generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(business_id) REFERENCES businesses(id)
    );
    """)
    conn.commit()

    # Seed demo data if no users exist
    existing = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing == 0:
        _seed_demo(c, conn)

    conn.close()


def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def _seed_demo(c, conn):
    # Create owner user
    c.execute(
        "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
        ("Arjun Sharma", "owner@arthix.com", _hash("demo123"), "Owner"),
    )
    uid = c.lastrowid

    # Create accountant
    c.execute(
        "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
        ("Priya Mehta", "accountant@arthix.com", _hash("demo123"), "Accountant"),
    )

    # Create business
    c.execute(
        "INSERT INTO businesses (user_id,name,category,currency) VALUES (?,?,?,?)",
        (uid, "Sharma General Store", "Retail", "INR"),
    )
    bid = c.lastrowid

    # Seed 90 days of transactions
    cats_income  = ["Product Sales", "Service Fees", "Online Sales", "Wholesale"]
    cats_expense = ["Rent", "Utilities", "Supplies", "Salaries", "Marketing", "Transport", "Maintenance"]

    today = date.today()
    for i in range(90):
        d = today - timedelta(days=i)
        # 1-3 sales per day
        for _ in range(random.randint(1, 3)):
            c.execute(
                "INSERT INTO transactions (business_id,type,category,amount,description,txn_date) VALUES (?,?,?,?,?,?)",
                (bid, "Income", random.choice(cats_income),
                 round(random.uniform(500, 8000), 2),
                 "Daily revenue entry", d.isoformat()),
            )
        # 0-2 expenses per day
        for _ in range(random.randint(0, 2)):
            c.execute(
                "INSERT INTO transactions (business_id,type,category,amount,description,txn_date) VALUES (?,?,?,?,?,?)",
                (bid, "Expense", random.choice(cats_expense),
                 round(random.uniform(100, 3000), 2),
                 "Operating expense", d.isoformat()),
            )

    # Seed products
    products = [
        ("Rice (5kg bag)", "RICE5", 180, 250, 120, 20),
        ("Refined Oil (1L)", "OIL1L", 95, 135, 85, 15),
        ("Sugar (1kg)", "SUG1K", 42, 58, 200, 30),
        ("Wheat Flour (10kg)", "WF10K", 290, 380, 65, 10),
        ("Dal Toor (500g)", "DAL500", 55, 80, 150, 25),
        ("Biscuits (Family Pk)", "BSC-F", 35, 55, 8, 20),
        ("Soap Bar (6pk)", "SOAP6", 120, 165, 45, 15),
        ("Shampoo (200ml)", "SHP200", 85, 130, 30, 10),
        ("Detergent (1kg)", "DET1K", 95, 140, 55, 12),
        ("Cold Drink (2L)", "CDK2L", 75, 110, 12, 20),
    ]
    for p in products:
        c.execute(
            "INSERT INTO products (business_id,name,sku,cost_price,sale_price,stock,low_stock_threshold) VALUES (?,?,?,?,?,?,?)",
            (bid, *p),
        )

    conn.commit()


# ── Auth ──────────────────────────────────────────────────────────────────────
def authenticate(email, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, _hash(password)),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def register_user(name, email, password, role="Owner"):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, _hash(password), role),
        )
        conn.commit()
        uid = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()[0]
        conn.close()
        return uid
    except sqlite3.IntegrityError:
        conn.close()
        return None


def create_business(user_id, name, category, currency="INR"):
    conn = get_conn()
    conn.execute(
        "INSERT INTO businesses (user_id,name,category,currency) VALUES (?,?,?,?)",
        (user_id, name, category, currency),
    )
    conn.commit()
    bid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return bid


def get_businesses(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM businesses WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Transactions ──────────────────────────────────────────────────────────────
def add_transaction(business_id, txn_type, category, amount, description, txn_date):
    conn = get_conn()
    conn.execute(
        "INSERT INTO transactions (business_id,type,category,amount,description,txn_date) VALUES (?,?,?,?,?,?)",
        (business_id, txn_type, category, amount, description, txn_date),
    )
    conn.commit()
    conn.close()


def get_transactions(business_id, start=None, end=None, txn_type=None):
    conn = get_conn()
    q = "SELECT * FROM transactions WHERE business_id=?"
    params = [business_id]
    if start:
        q += " AND txn_date >= ?"; params.append(start)
    if end:
        q += " AND txn_date <= ?"; params.append(end)
    if txn_type:
        q += " AND type=?"; params.append(txn_type)
    q += " ORDER BY txn_date DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_transaction(txn_id):
    conn = get_conn()
    conn.execute("DELETE FROM transactions WHERE id=?", (txn_id,))
    conn.commit()
    conn.close()


def update_transaction(txn_id, category, amount, description, txn_date):
    conn = get_conn()
    conn.execute(
        "UPDATE transactions SET category=?,amount=?,description=?,txn_date=? WHERE id=?",
        (category, amount, description, txn_date, txn_id),
    )
    conn.commit()
    conn.close()


# ── Products / Inventory ──────────────────────────────────────────────────────
def get_products(business_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM products WHERE business_id=?", (business_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_product(business_id, name, sku, cost_price, sale_price, stock, threshold):
    conn = get_conn()
    conn.execute(
        "INSERT INTO products (business_id,name,sku,cost_price,sale_price,stock,low_stock_threshold) VALUES (?,?,?,?,?,?,?)",
        (business_id, name, sku, cost_price, sale_price, stock, threshold),
    )
    conn.commit()
    conn.close()


def update_stock(product_id, change, reason):
    conn = get_conn()
    conn.execute("UPDATE products SET stock = stock + ? WHERE id=?", (change, product_id))
    conn.execute(
        "INSERT INTO inventory_logs (product_id,change,reason) VALUES (?,?,?)",
        (product_id, change, reason),
    )
    conn.commit()
    conn.close()


def get_inventory_logs(business_id):
    conn = get_conn()
    rows = conn.execute("""
        SELECT il.*, p.name as product_name FROM inventory_logs il
        JOIN products p ON il.product_id = p.id
        WHERE p.business_id=?
        ORDER BY il.logged_at DESC LIMIT 100
    """, (business_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Analytics helpers ─────────────────────────────────────────────────────────
def get_daily_summary(business_id, days=30):
    import pandas as pd
    txns = get_transactions(business_id)
    if not txns:
        return pd.DataFrame()
    df = pd.DataFrame(txns)
    df["txn_date"] = pd.to_datetime(df["txn_date"])
    df["amount"] = df["amount"].astype(float)
    pivot = df.pivot_table(index="txn_date", columns="type", values="amount", aggfunc="sum").fillna(0)
    pivot.columns = [c.lower() for c in pivot.columns]
    if "income" not in pivot.columns:   pivot["income"]  = 0
    if "expense" not in pivot.columns:  pivot["expense"] = 0
    pivot["profit"] = pivot["income"] - pivot["expense"]
    return pivot.reset_index().tail(days)


def get_category_summary(business_id):
    import pandas as pd
    txns = get_transactions(business_id)
    if not txns:
        return pd.DataFrame(), pd.DataFrame()
    df = pd.DataFrame(txns)
    df["amount"] = df["amount"].astype(float)
    inc = df[df["type"] == "Income"].groupby("category")["amount"].sum().reset_index()
    exp = df[df["type"] == "Expense"].groupby("category")["amount"].sum().reset_index()
    return inc, exp


# ── Users (admin) ─────────────────────────────────────────────────────────────
def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id,name,email,role,created_at FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_businesses():
    conn = get_conn()
    rows = conn.execute("""
        SELECT b.*, u.name as owner_name FROM businesses b
        JOIN users u ON b.user_id = u.id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
