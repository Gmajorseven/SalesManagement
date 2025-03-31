# routes/product_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

# Create a Blueprint for product routes
product_bp = Blueprint('product_bp', __name__)

DATABASE = './db/store.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to show products with pagination
@product_bp.route('/products')
def products():
    try:
        conn = get_db_connection()
        # Set the number of products per page
        per_page = 5
        
        # Get the current page from query params (default is 1)
        page = request.args.get('page', 1, type=int)
        
        # Calculate the offset for the query
        offset = (page - 1) * per_page
        
        # Query for the products with pagination
        products = conn.execute('''SELECT Products.pro_id, Products.name, Products.price, Products.unit, Products.qty, Product_categories.name AS category
        FROM Products JOIN Product_categories ON Products.category_id = Product_categories.proc_id LIMIT ? OFFSET ?''', (per_page, offset)).fetchall()

        # Get the total number of products for pagination
        total_products = conn.execute('SELECT COUNT(*) FROM Products').fetchone()[0]
        
        # Calculate total number of pages
        total_pages = (total_products + per_page - 1) // per_page
        
        conn.close()
        
        # Determine if we have a previous or next page
        has_prev = page > 1
        has_next = page < total_pages
        
        return render_template('products.html', 
                               products=products,
                               page=page, 
                               total_pages=total_pages,
                               has_prev=has_prev,
                               has_next=has_next)

    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return render_template('products.html', products=[])

# Route to add a new product
@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        qty = request.form['qty']
        category = request.form['category']
        print(category)
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO Products (name, price, unit, qty, category_id) VALUES (?, ?, ?, ?, ?)', 
                         (name, price, unit, qty, category))
            conn.commit()
            conn.close()
            flash('Product added successfully!', 'success')
            return redirect(url_for('product_bp.products'))

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
            return redirect(url_for('product_bp.add_product'))

    else:
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM Product_categories').fetchall()
        conn.close()
        return render_template('add_product.html', categories=categories)

# Route to edit an existing product
@product_bp.route('/edit_product/<int:pro_id>', methods=['GET', 'POST'])
def edit_product(pro_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM Products WHERE pro_id = ?', (pro_id,)).fetchone()
    categories = conn.execute('SELECT * FROM Product_categories').fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        unit = request.form['unit']
        qty = request.form['qty']
        category = request.form['category']

        try:
            conn.execute('UPDATE Products SET name = ?, price = ?, unit = ?, qty = ?, category = ? WHERE pro_id = ?', 
                         (name, price, unit, qty, category, pro_id))
            conn.commit()
            conn.close()
            flash('Product updated successfully!', 'info')
            return redirect(url_for('product_bp.products'))
        
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
            return redirect(url_for('product_bp.edit_product', pro_id=pro_id))

    conn.close()
    return render_template('edit_product.html', product=product, categories=categories)

# Route to delete a product
@product_bp.route('/delete_product/<int:pro_id>')
def delete_product(pro_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Products WHERE pro_id = ?', (pro_id,))
    conn.commit()
    conn.close()
    flash('Product deleted!', 'danger')
    return redirect(url_for('product_bp.products'))

