# routes/add_sales_transaction.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

# Create a Blueprint for add_sales_transaction routes
add_sales_transaction_bp = Blueprint('add_sales_transaction_bp', __name__)

DATABASE = './db/store.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to add sales transaction
@add_sales_transaction_bp.route('/add_sales_transaction', methods=['GET', 'POST'])
def add_sales_transaction():
    try:
        conn = get_db_connection()
        customers = conn.execute('SELECT * FROM Customers').fetchall()
        salespersons = conn.execute('SELECT * FROM Salespersons').fetchall()
        products = conn.execute('SELECT * FROM Products').fetchall()

        if request.method == 'POST':
            cus_id = request.form['cus_id']
            sp_id = request.form['sp_id']
            st_total = request.form['st_total']
            product_ids = request.form.getlist('product_id')
            quantities = request.form.getlist('quantity')

            # Insert sales transaction
            cur = conn.cursor()
            cur.execute('INSERT INTO Sales_transactions (cus_id, sp_id, st_total) VALUES (?, ?, ?)',
                        (cus_id, sp_id, st_total))
            st_id = cur.lastrowid  # Get the new transaction ID
            status = 'Completed'
            # Insert products sold
            for i in range(len(product_ids)):
                cur.execute('INSERT INTO Sales_products (sales_transaction_id, product_id, purchased_qty, status) VALUES (?, ?, ?, ?)',
                            (st_id, product_ids[i], quantities[i], status))
                cur.execute('UPDATE Products SET qty = qty - ? WHERE pro_id = ?', (quantities[i], product_ids[i]))
                # Check if the quantity is sufficient
                qty_check = cur.execute('SELECT name, qty from Products WHERE pro_id = ?', product_ids[i]).fetchall()
                #if qty_check[0]['qty'] <= 10:
                #    flash(f"Warning: Product {qty_check[0]['name']} is running low on stock!", 'warning') 
                #    cur.execute('UPDATE Products SET reorder_point = ? WHERE pro_id = ?','True', (product_ids[i],))
                
                print(qty_check[0]['name'], qty_check[0]['qty'])

            conn.commit()
            conn.close()

            flash('Sales transaction added successfully!', 'success')
            return redirect(url_for('add_sales_transaction_bp.add_sales_transaction'))

        conn.close()
        return render_template('add_sales_transaction.html', customers=customers, salespersons=salespersons, products=products)
    except Exception as e:
        flash(f"Error adding sales transaction: {str(e)}", 'danger')
        print("Error:", e)
        return redirect(url_for('add_sales_transaction_bp.add_sales_transaction'))