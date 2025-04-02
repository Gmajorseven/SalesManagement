import sqlite3

DB = 'store.db'

def updateSalestransaction():
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        check_status = 'Pending'
        cursor.execute("SELECT DISTINCT sales_transaction_id FROM Sales_products WHERE status = ?", (check_status,))
        bills_id = [item[0] for item in cursor.fetchall()]
        
        for i in range(len(bills_id)):
            bill_id = bills_id[i]
            cursor.execute('''
                UPDATE Sales_transactions SET st_total = (SELECT SUM(Products.price * Sales_products.purchased_qty) as st_total
                FROM Products INNER JOIN Sales_products ON Products.pro_id = Sales_products.product_id WHERE sales_transaction_id = ?)
                WHERE st_id = ?;
            ''', (bill_id, bill_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Error accessing database:", e)

def updateProductandSalingstatus():
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT product_id FROM Sales_products")
        pro_ids = [item[0] for item in cursor.fetchall()]

        for i in range(len(pro_ids)):
            pro_id = pro_ids[i]
            check_status = 'Pending'
            cursor.execute('''
                UPDATE Products SET qty = qty - (SELECT SUM(purchased_qty) as minus_qty FROM Sales_products WHERE product_id = Products.pro_id
                AND status = ?) WHERE pro_id = ?;
            ''', (check_status, pro_id))
            new_status = 'Completed'
            cursor.execute('''
                UPDATE Sales_products SET status = ? WHERE product_id = ?
            ''', (new_status, pro_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Error accessing database", e)

def main():
    updateSalestransaction()
    updateProductandSalingstatus()
    print("Update Total Sales transaction and Saling status successfully!")
if __name__ == "__main__":
    main()
