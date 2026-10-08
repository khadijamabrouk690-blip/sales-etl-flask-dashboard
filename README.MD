# Sales ETL Pipeline + Flask Dashboard

End-to-end pipeline: ingest three sources (CSV + Parquet + URL), clean and merge them in Pandas, load the final Sales table into SQL Server, and serve it with Flask.

## Data Sources

- `customers.csv` - customer_id, first_name, last_name, city, age, email
- `orders.parquet` - order_id, customer_id, product_id, quantity, order_date
- `products.csv` (URL) - https://raw.githubusercontent.com/MohammedHameds/test1455/refs/heads/main/products.csv

## Pipeline

1. **Customers:** drop duplicates, `fillna(email)`, build `Full_name`, standardize `city` with `strip + title`, `to_numeric(age)`, keep `customer_id, city, age, email, Full_name`
2. **Orders:** drop duplicate `order_id`, `to_datetime(order_date)`, `to_numeric(quantity, customer_id, product_id)`
3. **Products:** drop duplicates, strip `product_name/category`, `to_numeric(unit_price)`
4. **Merge:** `orders + customers on customer_id (inner)`, then `+ products on product_id (inner)`
5. **Calculate:** `total_price = quantity * unit_price`
6. **Final table `sales1`:** `order_id, customer, product, quantity, unit_price, total_price` (renamed from `Full_name, product_name`)
7. **Load:** create SQL Server table `sales` in `salesDB` and insert with `pyodbc.executemany`

## SQL Setup

Requires local SQL Server with ODBC Driver 17 and a database named `salesDB`. The notebook creates:

```sql
create table sales (
    order_id INT,
    customer varchar(255),
    product varchar(255),
    quantity int,
    unit_price float,
    total_price float
)
```

Connection uses Windows auth: `Trusted_Connection=yes`.

## Flask App

`app.py` connects to the same DB, reads `select * from sales`, and renders `templates/index.html` at `/`.

## Project Structure

```text
flask/
├── Task.ipynb
├── app.py
├── customers.csv
├── orders.parquet
├── templates/
│   └── index.html
└── README.md
```

## How to Run

```bash
pip install pandas pyarrow flask pyodbc
```

1. Open `Task.ipynb` -> Restart + Run All (builds `sales` in SQL Server).
2. Start the dashboard:

```bash
cd flask
python app.py
```

3. Open http://127.0.0.1:5001

## Tools

Python, Pandas, PyArrow, SQL Server + pyodbc, Flask, HTML
