# routes/customer_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

# Create a Blueprint for customer routes
customer_bp = Blueprint('customer_bp', __name__)

DATABASE = './db/store.db'
CUSTOMERS_PER_PAGE = 5  # Number of customers to show per page

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Customers Route with pagination
@customer_bp.route('/customers')
def customers():
    try:
        # Get the current page from the query parameter (default to 1 if not specified)
        page = request.args.get('page', 1, type=int)
        
        # Calculate the offset for SQL query
        offset = (page - 1) * CUSTOMERS_PER_PAGE
        
        conn = get_db_connection()
        
        # Fetch customers for the current page
        customers = conn.execute('SELECT * FROM Customers LIMIT ? OFFSET ?', (CUSTOMERS_PER_PAGE, offset)).fetchall()
        conn.close()
        
        # Fetch the total number of customers to calculate total pages
        conn = get_db_connection()
        total_customers = conn.execute('SELECT COUNT(*) FROM Customers').fetchone()[0]
        conn.close()
        
        # Calculate the total number of pages
        total_pages = (total_customers + CUSTOMERS_PER_PAGE - 1) // CUSTOMERS_PER_PAGE
        
        # Determine if there are previous and next pages
        has_prev = page > 1
        has_next = page < total_pages
        
        return render_template('customers.html', customers=customers, page=page, total_pages=total_pages, has_prev=has_prev, has_next=has_next)
    
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return render_template('customers.html', customers=[])

# Add Customer Route
@customer_bp.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    email = request.form['email']
    tel = request.form['tel']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO Customers (name, email, tel) VALUES (?, ?, ?)', (name, email, tel))
    conn.commit()
    conn.close()
    
    flash('Customer added successfully!', 'success')
    return redirect(url_for('customer_bp.customers'))

# Edit Customer Route
@customer_bp.route('/edit_customer/<int:cus_id>', methods=['GET', 'POST'])
def edit_customer(cus_id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM Customers WHERE cus_id = ?', (cus_id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        conn.execute('UPDATE Customers SET name = ?, email = ?, tel = ? WHERE cus_id = ?', (name, email, tel, cus_id))
        conn.commit()
        conn.close()
        flash('Customer updated successfully!', 'info')
        return redirect(url_for('customer_bp.customers'))
    
    conn.close()
    return render_template('edit_customer.html', customer=customer)

# Delete Customer Route
@customer_bp.route('/delete_customer/<int:cus_id>')
def delete_customer(cus_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Customers WHERE cus_id = ?', (cus_id,))
    conn.commit()
    conn.close()
    flash('Customer deleted!', 'danger')
    return redirect(url_for('customer_bp.customers'))

