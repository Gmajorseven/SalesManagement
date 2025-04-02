# app.py
from flask import Flask, render_template
from routes import customer_bp, category_bp, product_bp  

app = Flask(__name__)
app.secret_key = 'secret_key'  # For flash messages

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Register the Blueprint
app.register_blueprint(customer_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

