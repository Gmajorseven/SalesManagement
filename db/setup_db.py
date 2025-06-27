import sqlite3

DATABASE = "store.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    cus_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(50) UNIQUE,
    tel VARCHAR(15) UNIQUE
); ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Salespersons (
    sp_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(50) UNIQUE,
    tel VARCHAR(15) UNIQUE,
    salary NUMERIC(10, 2) NOT NULL CHECK(salary >= 0)
); ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Product_categories (
    proc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
); ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    pro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    unit TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK(qty >= 0),
    category_id INTEGER NOT NULL,
    reorder_point BOOLEAN CHECK(reorder_point IN (1, 0)) DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES Product_categories(proc_id) ON DELETE CASCADE
); ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Sales_transactions (
    st_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    st_date TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    st_total NUMERIC(10, 2) DEFAULT 0 CHECK(st_total >= 0),
    cus_id INTEGER NOT NULL,
    sp_id INTEGER NOT NULL,
    FOREIGN KEY (cus_id) REFERENCES Customers (cus_id) ON DELETE CASCADE,
    FOREIGN KEY (sp_id) REFERENCES Salespersons (sp_id) ON DELETE CASCADE
); ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Sales_products (
    sales_transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    purchased_qty INTEGER NOT NULL CHECK(purchased_qty > 0),
    status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (sales_transaction_id) REFERENCES Sales_transactions (st_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products (pro_id) ON DELETE CASCADE,
    PRIMARY KEY (sales_transaction_id, product_id)
); ''')

conn.commit()
conn.close()
print("Database initialized successfully.")
