# Sales Management System

A simple Flask-based web application for managing sales, customers, products, and product categories.

## Features

*   **Customer Management:** Add, edit, and delete customer information.
*   **Product Management:** Add, edit, and delete products.
*   **Category Management:** Add, edit, and delete product categories.
*   **Sales Transactions:** Add new sales transactions and view transaction details.
*   **Sales Filtering:** Filter sales records by date, product, category, or salesperson.
*   **Low Stock Alerts:** Get warnings when product quantities are running low.

## Database Schema

The application uses an SQLite database with the following tables:

*   `Customers`: Stores customer information (name, email, telephone).
*   `Salespersons`: Stores salesperson information (name, email, telephone, salary).
*   `Product_categories`: Stores product category information (name).
*   `Products`: Stores product information (name, price, unit, quantity, category, reorder point).
*   `Sales_transactions`: Stores sales transaction information (date, total, customer, salesperson).
*   `Sales_products`: A linking table for sales transactions and products.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/SalesManagement.git
    cd SalesManagement
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirement.txt
    ```

4.  **Initialize the database:**
    ```bash
    python db/setup_db.py
    ```

5.  **Run the application:**
    ```bash
    flask run
    ```

The application will be available at `http://127.0.0.1:5000`.

## Dependencies

The project uses the following Python packages:

*   Flask
*   python-dotenv
*   Faker (for generating dummy data)
*   pysqlite3

## Routes

*   `/`: Home page with links to other sections.
*   `/customers`: View, add, edit, and delete customers. Also, filter sales transactions.
*   `/categories`: View, add, edit, and delete product categories.
*   `/products`: View, add, edit, and delete products.
*   `/add_sales_transaction`: Add a new sales transaction.
