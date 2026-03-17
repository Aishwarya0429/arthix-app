# 📊 Arthix — Small Business Sales & Profit Analyzer

> An open-source, full-featured analytics platform for small and micro-business owners.
> Built with Python + Streamlit. No subscriptions. No complexity.

---

## 🚀 Features

### ✅ Milestone 1 — Authentication & Transaction Logging
- Secure login with SHA-256 password hashing
- JWT-ready session management
- Multi-business profile support per user
- Role-based access: **Owner**, **Accountant**, **Staff**
- Quick daily transaction logging (Income & Expense)

### ✅ Milestone 2 — Profit & Inventory Tracking
- Automatic daily/weekly/monthly profit calculation
- Inventory tracking with COGS computation
- Low-stock and out-of-stock alerts
- Stock adjustment log with reasons

### ✅ Milestone 3 — Analytics & AI Forecasting
- Interactive multi-metric area & bar charts (Plotly)
- Category-wise income and expense breakdowns
- AI-powered sales & profit forecasting (Linear Regression + trend)
- Confidence interval bands on forecasts
- Profit margin trend analysis

### ✅ Milestone 4 — Reports, Admin & Deployment
- PDF report generation (ReportLab) with branding
- Excel workbook export (multi-sheet, openpyxl)
- Admin dashboard: user management, system health monitor
- Docker-ready (add `Dockerfile` for containerization)

---

## 🛠️ Tech Stack

| Layer           | Technology                          |
|----------------|--------------------------------------|
| Frontend/UI    | Streamlit 1.32+                      |
| Charts         | Plotly 5.x                           |
| Data           | Pandas, NumPy                        |
| Database       | SQLite (via Python sqlite3)          |
| ML / Forecast  | scikit-learn (Linear Regression)     |
| PDF Reports    | ReportLab                            |
| Excel Reports  | openpyxl                             |
| Auth           | SHA-256 + PyJWT                      |
| Styling        | Custom CSS (dark theme, Syne + DM Sans fonts) |

---

## 📦 Installation & Setup

### 1. Clone / Download
```bash
git clone https://github.com/yourname/arthix.git
cd arthix
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🔐 Demo Login

| Role        | Email                         | Password  |
|-------------|-------------------------------|-----------|
| Owner       | owner@arthix.com            | demo123   |
| Accountant  | accountant@arthix.com       | demo123   |

> Demo data includes 90 days of pre-seeded transactions and 10 inventory products.

---

## 📁 Project Structure

```
arthix/
├── app.py                      # Main entry point & router
├── arthix.db                 # SQLite database (auto-created)
├── requirements.txt
├── .streamlit/
│   └── config.toml             # Dark theme config
├── pages/
│   ├── auth_page.py            # Login & Registration
│   ├── dashboard.py            # Main overview dashboard
│   ├── transactions.py         # Add/Edit/Delete transactions
│   ├── inventory.py            # Stock management & COGS
│   ├── analytics.py            # Charts & AI forecasting
│   ├── reports.py              # PDF & Excel report generation
│   ├── admin.py                # Admin panel (Owner only)
│   └── profile.py              # User & business profile
└── utils/
    ├── database.py             # All DB operations (SQLite)
    ├── auth.py                 # Session authentication
    ├── theme.py                # Global CSS dark theme
    ├── charts.py               # Plotly chart helpers
    └── forecasting.py          # AI forecasting engine
```

---

## 🗄️ Data Schema

### Users
| Field      | Type     |
|-----------|----------|
| id         | INTEGER PK |
| name       | TEXT     |
| email      | TEXT UNIQUE |
| password   | TEXT (hashed) |
| role       | TEXT     |
| created_at | DATETIME |

### Businesses
| Field      | Type     |
|-----------|----------|
| id         | INTEGER PK |
| user_id    | FK → users |
| name       | TEXT     |
| category   | TEXT     |
| currency   | TEXT     |

### Transactions
| Field       | Type     |
|------------|----------|
| id          | INTEGER PK |
| business_id | FK → businesses |
| type        | TEXT (Income/Expense) |
| category    | TEXT     |
| amount      | REAL     |
| txn_date    | DATE     |
| description | TEXT     |

### Products (Inventory)
| Field               | Type    |
|--------------------|---------|
| id                  | INTEGER PK |
| business_id         | FK      |
| name, sku           | TEXT    |
| cost_price, sale_price | REAL |
| stock               | INTEGER |
| low_stock_threshold | INTEGER |

### Reports
| Field        | Type    |
|-------------|---------|
| id           | INTEGER PK |
| business_id  | FK      |
| report_type  | TEXT    |
| file_path    | TEXT    |
| generated_at | DATETIME |

---

## 🔮 AI Forecasting

The forecasting engine uses **Linear Regression** (sklearn-style, implemented with NumPy polyfit) to project:
- Future Revenue
- Future Expenses  
- Net Profit

**Confidence bands** (90% CI) are calculated from residual standard deviation.

To upgrade to Prophet (Facebook):
```bash
pip install prophet
```
Replace `utils/forecasting.py` with Prophet model.

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

Build & run:
```bash
docker build -t arthix .
docker run -p 8501:8501 arthix
```

---

## 📈 Evaluation Milestones

| Milestone       | Status  | Features                                      |
|----------------|---------|-----------------------------------------------|
| Week 1–2        | ✅ Done | Auth, JWT sessions, transaction logging        |
| Week 3–4        | ✅ Done | Profit calc, inventory, COGS, low-stock alerts |
| Week 5–6        | ✅ Done | Analytics dashboard, AI forecasting, charts    |
| Week 7–8        | ✅ Done | PDF/Excel reports, Admin panel, deployment     |

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

*Built with ❤️ using Python & Streamlit · Infosys Springboard Project*
