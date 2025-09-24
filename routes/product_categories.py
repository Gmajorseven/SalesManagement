# routes/category_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db.conn_db import get_db_connection

# Create a Blueprint for category routes
category_bp = Blueprint('category_bp', __name__)

# Route to show categories
@category_bp.route('/categories')
def categories():
    try:
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM Product_categories').fetchall()
        conn.close()
        return render_template('categories.html', categories=categories)
    
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return render_template('categories.html', categories=[])

# Route to add a new category
@category_bp.route('/add_category', methods=['POST'])
def add_category():
    try:    
        name = request.form['name']
    
        conn = get_db_connection()
        conn.execute('INSERT INTO Product_categories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
    
        flash('Category added successfully!', 'success')

    except Exception as e:
        flash(f"Error adding category: {str(e)}", 'danger')

    return redirect(url_for('category_bp.categories'))

# Route to edit an existing category
@category_bp.route('/edit_category/<int:proc_id>', methods=['GET', 'POST'])
def edit_category(proc_id):
    try:
        conn = get_db_connection()
        category = conn.execute('SELECT * FROM Product_categories WHERE proc_id = ?', (proc_id,)).fetchone()
    
        if request.method == 'POST':
            name = request.form['name']
        
            conn.execute('UPDATE Product_categories SET name = ? WHERE proc_id = ?', (name, proc_id))
            conn.commit()
            conn.close()
            flash('Category updated successfully!', 'info')
            return redirect(url_for('category_bp.categories'))
    
        conn.close()
        return render_template('edit_category.html', category=category)

    except Exception as e:
        flash(f"Error updating category: {str(e)}", 'danger')
        return redirect(url_for('caregory_bp.categories'))

# Route to delete a category
@category_bp.route('/delete_category/<int:proc_id>')
def delete_category(proc_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Product_categories WHERE proc_id = ?', (proc_id,))
    conn.commit()
    conn.close()
    flash('Category deleted!', 'danger')
    return redirect(url_for('category_bp.categories'))

