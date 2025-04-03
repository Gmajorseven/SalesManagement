import pysqlite3 as sqlite3
from faker import Faker

fake = Faker()
DB = 'store.db'

def create_database():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers(
            cus_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            name VARCHAR(30) NOT NULL,
            email VARCHAR(30) UNIQUE,
            tel VARCHAR(15) UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

def fake_phone_number(fake: Faker) -> str:
    return f'+66{fake.unique.msisdn()[4:]}'


def insert_customers(n=100):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    for _ in range(n):
        name = fake.name()
        email = fake.unique.email()
        tel = fake_phone_number(fake)

        cursor.execute("INSERT OR IGNORE INTO Customers(name, email, tel) VALUES(?, ?, ?)", (name, email, tel))

    conn.commit()
    conn.close()

def main():
    create_database()
    insert_customers(100)
    print("Database and customer records created successfully!")

if __name__ == "__main__":
    main()
