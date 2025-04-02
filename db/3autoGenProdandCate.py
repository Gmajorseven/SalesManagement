import sqlite3
from faker import Faker
import random

# Initialize Faker
fake = Faker()

DB = 'store.db'

def create_database():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # Create product category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product_categories (
            proc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Create product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            pro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            unit TEXT NOT NULL,
            qty INTEGER NOT NULL CHECK(qty >= 0),
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES Product_categories(proc_id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_product_categories(categories):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    for category in categories:
        cursor.execute("INSERT OR IGNORE INTO Product_categories (name) VALUES (?)", (category,))
    
    conn.commit()
    conn.close()

def insert_products(n=51):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    category_map = {
        "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch", "Monitor", "Camera", "Speaker"],
        "Furniture": ["Chair", "Table", "Sofa", "Bed", "Cabinet", "Desk", "Bookshelf", "Wardrobe"],
        "Clothing": ["T-shirt", "Jeans", "Jacket", "Sweater", "Dress", "Shorts", "Hoodie", "Scarf"],
        "Books": ["Novel", "Textbook", "Comic", "Magazine", "Biography", "Poetry", "Encyclopedia", "Cookbook"],
        "Toys": ["Doll", "Action Figure", "Puzzle", "Board Game", "Lego Set", "Remote Control Car", "Plush Toy", "Building Blocks"],
        "Kitchen Appliances": ["Blender", "Toaster", "Microwave", "Refrigerator", "Oven", "Dishwasher", "Coffee Maker", "Air Fryer"],
        "Sports Equipment": ["Basketball", "Football", "Tennis Racket", "Dumbbells", "Yoga Mat", "Bicycle", "Helmet", "Running Shoes"]
    }
    
    units_map = {
        "Electronics": "piece",
        "Furniture": "set",
        "Clothing": "item",
        "Books": "book",
        "Toys": "piece",
        "Kitchen Appliances": "unit",
        "Sports Equipment": "piece"
    }
    
    cursor.execute("SELECT proc_id, name FROM Product_categories")
    category_dict = {row[1]: row[0] for row in cursor.fetchall()}
    
    for category, products in category_map.items():
        if category in category_dict:
            category_id = category_dict[category]
            unit = units_map.get(category, "unit")
            for _ in range(n // len(category_map)):
                name = random.choice(products)
                price = round(random.uniform(5, 500), 2)
                qty = random.randint(50, 100)
                cursor.execute("INSERT INTO Products (name, price, unit, qty, category_id) VALUES (?, ?, ?, ?, ?)",
                               (name, price, unit, qty, category_id))
    
    conn.commit()
    conn.close()

def main():
    create_database()
    categories = ["Electronics", "Furniture", "Clothing", "Books", "Toys", "Kitchen Appliances", "Sports Equipment"]
    insert_product_categories(categories)
    insert_products(51)
    print("Product database with meaningful categories and products created successfully!")

if __name__ == "__main__":
    main()

