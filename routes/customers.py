# routes/customer_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db.conn_db import get_db_connection

# Create a Blueprint for customer routes
customer_bp = Blueprint('customer_bp', __name__)

CUSTOMERS_PER_PAGE = 10  # Number of customers to show per page

# Customers Route with pagination
@customer_bp.route('/customers', methods=['GET', 'POST'])
def customers():
    try:
        # Get the current page from the query parameter (default to 1 if not specified)
        page = request.args.get('page', 1, type=int)
        
        # Calculate the offset for SQL query
        offset = (page - 1) * CUSTOMERS_PER_PAGE
        
        conn = get_db_connection()
        
        # Fetch customers for the current page
        fcustomers = conn.execute('SELECT * FROM Customers LIMIT ? OFFSET ?', (CUSTOMERS_PER_PAGE, offset)).fetchall()
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

        conn = get_db_connection()
        customers = conn.execute('SELECT * FROM Customers').fetchall()
        categories = conn.execute('SELECT * FROM Product_categories').fetchall()
        products = conn.execute('SELECT * FROM Products').fetchall()
        salespersons = conn.execute('SELECT * FROM Salespersons').fetchall()

        filtered_sales = []  # Default: No sales shown until filtered
        query_params = []

        if request.method == 'POST':
            year = request.form.get('year')
            month = request.form.get('month')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            product_id = request.form.get('product_id')
            category_id = request.form.get('category_id')
            salesperson_id = request.form.get('salesperson_id')

        # Apply Filters to Query
            query = """
                SELECT Sales_transactions.st_id, Sales_transactions.st_date, Sales_transactions.st_total, Customers.name AS customer, Salespersons.name AS salesperson,
                Products.name AS product, Products.price, Sales_products.purchased_qty, Product_categories.name AS category
                FROM Sales_transactions
                JOIN Sales_products ON Sales_transactions.st_id = Sales_products.sales_transaction_id
                JOIN Products ON Sales_products.product_id = Products.pro_id
                JOIN Product_categories ON Products.category_id = Product_categories.proc_id
                JOIN Customers ON Sales_transactions.cus_id = Customers.cus_id
                JOIN Salespersons ON Sales_transactions.sp_id = Salespersons.sp_id
                WHERE 1=1
            """

            if year:
                query += " AND strftime('%Y', Sales_transactions.st_date) = ?"
                query_params.append(year)

            if month:
                query += " AND strftime('%m', Sales_transactions.st_date) = ?"
                query_params.append(month)

            if start_date and end_date:
                query += " AND Sales_transactions.st_date BETWEEN ? AND ?"
                query_params.append(start_date)
                query_params.append(end_date)

            if product_id:
                query += " AND Products.pro_id = ?"
                query_params.append(product_id)

            if category_id:
                query += " AND Product_categories.proc_id = ?"
                query_params.append(category_id)

            if salesperson_id:
                query += " AND Salespersons.sp_id = ?"
                query_params.append(salesperson_id)

            filtered_sales = conn.execute(query, query_params).fetchall()
        else:
            filtered_sales = []  # Default: No data unless searched

        conn.close()

        
        return render_template('customers.html', fcustomers=fcustomers, 
                                                 page=page, 
                                                 total_pages=total_pages, 
                                                 has_prev=has_prev, 
                                                 has_next=has_next, 
                                                 customers=customers, 
                                                 categories=categories, 
                                                 products=products, 
                                                 salespersons=salespersons, 
                                                 sales=filtered_sales,)
    
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        print("Error:", e)
        return render_template('customers.html', customers=[])

# Add Customer Route
@customer_bp.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
    
        conn = get_db_connection()
        conn.execute('INSERT INTO Customers (name, email, tel) VALUES (?, ?, ?)', (name, email, tel))
        conn.commit()
        conn.close()
    
        flash('Customer added successfully!', 'success')
    except Exception as e:
        flash(f"Error adding customer: {str(e)}", 'danger')

    return redirect(url_for('customer_bp.customers'))

# Edit Customer Route
@customer_bp.route('/edit_customer/<int:cus_id>', methods=['GET', 'POST'])
def edit_customer(cus_id):
    try:
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

    except Exception as e:
        flash(f"Error updating customer: {str(e)}", 'danger')
        return redirect(url_for('customer_bp.customers'))

# Delete Customer Route
@customer_bp.route('/delete_customer/<int:cus_id>')
def delete_customer(cus_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Customers WHERE cus_id = ?', (cus_id,))
        conn.commit()
        conn.close()
        flash('Customer deleted!', 'danger')
    
    except Exception as e:
        flash(f"Error deleting customer: {str(e)}", 'danger')

    return redirect(url_for('customer_bp.customers'))

# Sales Price Overview Route
