import pysqlite3 as sqlite3
import random
from datetime import datetime

DB = 'store.db'

def create_database(): 
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales_transactions (
            st_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            st_date DATE DEFAULT (datetime('now', 'localtime')),
            st_total NUMERIC(10, 2) DEFAULT 0 CHECK(st_total >= 0),
            cus_id INTEGER NOT NULL,
            sp_id INTEGER NOT NULL,
            FOREIGN KEY (cus_id) REFERENCES Customers (cus_id) ON DELETE CASCADE,
            FOREIGN KEY (sp_id) REFERENCES Salespersons (sp_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales_products (
            sales_transaction_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            purchased_qty INTEGER NOT NULL CHECK(purchased_qty > 0),
            status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (sales_transaction_id) REFERENCES Sales_transactions (st_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES Products (pro_id) ON DELETE CASCADE,
            PRIMARY KEY (sales_transaction_id, product_id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_salestransaction(n=50):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        for _ in range(n):
            cus_id = random.randint(1, 100)
            sp_id = random.randint(1, 10)

            cursor.execute("INSERT INTO Sales_transactions (cus_id, sp_id) VALUES (?, ?)", (cus_id, sp_id))

        conn.commit()
        conn.close()
    
    except sqlite3.Error as e:
        print("Error accessing database:", e)

def insert_salingproducts():
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("SELECT st_id FROM Sales_transactions WHERE st_total = 0")
        sts_id = [item[0] for item in cursor.fetchall()]
        for i in range(len(sts_id)):
            st_id = sts_id[i]

            for j in range(random.randint(1, 5)):
                pro_id = random.randint(1, 49)
                buyed_qty = random.randint(1, 3)

                cursor.execute("INSERT OR IGNORE INTO Sales_products (sales_transaction_id, product_id, purchased_qty) VALUES (?, ?, ?)", (st_id, pro_id, buyed_qty))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error accessing database:", e)

def main():
    create_database()
    insert_salestransaction(50)
    insert_salingproducts()
    print("Database sales transaction and saling products records created successfully!")

if __name__ == "__main__":
    main()



