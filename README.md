# RFM Customer Segmentation

A reproducible, end-to-end RFM (Recency, Frequency, Monetary) analysis pipeline  
for an international retail company, with synthetic data generation.

📊 RFM Methodology

Recency (R): Days since a customer’s last purchase.
Frequency (F): Count of orders per customer.
Monetary (M): Total spend per customer.
Each dimension is scored 1–5 using pandas’ qcut (quintiles):

R: lower recency_days ⇒ higher R score.
F, M: higher frequency/spend ⇒ higher scores.
We then concatenate R F M into a 3-digit segment (e.g. 555 = best customers) and sum the scores into an overall rfm_score.

## Project Structure

    .
    ├── .gitignore
    ├── pyproject.toml
    ├── README.md
    ├── .venv/ # Virtual environment (gitignored)
    ├── data/
    │ ├── raw/
    │ │ ├── customers.csv # Synthetic customer profiles
    │ │ ├── orders.csv # Synthetic orders
    │ │ └── joined_orders.csv # SQL join output
    │ ├── processed/
    │ │ └── rfm_scores.csv # Final RFM results
    │ └── rfm.db # SQLite database with customers & orders tables
    ├── sql/
    │ ├── create_tables.sql # DDL: schema for customers & orders
    │ └── queries/
    │ └── extract_orders.sql -- SELECT joining orders↔customers
    ├── src/
    │ ├── init.py
    │ ├── synthetic_data.py # Generates data, applies DDL, writes to SQLite & CSV
    │ ├── data_engineering.py # Loads joined data & saves RFM CSV
    │ ├── rfm.py # Pure RFM scoring logic
    │ ├── utils.py # Directory, SQL, date helpers
    │ └── run_pipeline.py # Orchestrator: load → parse → compute → save
    ├── notebooks/
    │ └── 01_EDA.ipynb # Exploratory Data Analysis & visualizations
    └── tests/
    └── test_rfm.py # Unit tests for the RFM logic

## ⚙️ Dependencies

- **Python ≥ 3.10**  
- **pandas**, **numpy**  
- **SQLAlchemy** + **SQLite** (via `sqlite://` connection)  
- **Faker** (for synthetic data)  
- **pytest** (for unit tests)  
- **matplotlib** (for EDA)  

## Getting Started
### . Clone & Initialize
```bash
git clone https://github.com/your-org/RFM.git
cd RFM
git init
```

### Install dependecies all at once:
### From project root, with .venv activated
```bash
pip install -e .
```
🔄 Pipeline Overview

Generate & load synthetic data
python -m src.synthetic_data
Executes sql/create_tables.sql
Generates customers & orders via Faker
Writes raw CSVs (data/raw/) & loads into rfm.db
Runs sql/queries/extract_orders.sql → data/raw/joined_orders.csv
Compute & save RFM scores
python -m src.run_pipeline
Loads joined data via data_engineering.load_joined_data()
Parses date columns (utils.parse_date_column)
Calls rfm.compute_rfm() for scoring & segmentation
Saves data/processed/rfm_scores.csv
Exploratory Data Analysis
Open notebooks/01_EDA.ipynb in Jupyter
Visualize distributions, time-lags, heatmaps, segment comparisons
Testing
pytest -v
Unit tests in tests/test_rfm.py validate your RFM logic

💾 SQL Files & Database

sql/create_tables.sql
DDL for customers and orders tables (with foreign key constraint).
sql/queries/extract_orders.sql
Joins orders ↔ customers, selects key fields.
data/rfm.db
SQLite file created by synthetic_data.py, containing:
customers(customer_id, signup_date)
orders(order_id, customer_id, order_date, order_amount)
Inspect with the SQLite CLI:

sqlite3 data/rfm.db
.tables
.schema customers
.schema orders
.exit

▶️ How to Run

Activate your venv
source .venv/bin/activate   # macOS/Linux
# or .venv\Scripts\Activate.ps1 on Windows
Install dependencies
pip install -e .
Generate & load data
python -m src.synthetic_data
Compute & save RFM
python -m src.run_pipeline
Explore in Jupyter
Launch notebooks/01_EDA.ipynb
Run cells to view EDA results
Run tests
pytest -v