import sqlite3
db = sqlite3.connect('store.db')
cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS products")

cur.execute("""CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT, 
            price REAL )""")

cur.execute("INSERT INTO products (name, category, price) VALUES ('Wireless Mouse', 'Electronics', 350)")
cur.execute("INSERT INTO products (name, category, price) VALUES ('Python Programming', 'Books', 450)")
cur.execute("INSERT INTO products (name, category, price) VALUES ('Cotton T-Shirt', 'Clothing', 250)")
cur.execute("INSERT INTO products (name, category, price) VALUES ('Stainless Steel Water Bottle', 'Home', 180)")
cur.execute("INSERT INTO products (name, category, price) VALUES ('Bluetooth Headphones', 'Electronics', 1200)")


cur.execute("SELECT * FROM products WHERE category = 'Electronics'")
electronics_data = cur.fetchall()
for row in electronics_data:
    print(row)

print ("___________")

data = cur.execute("SELECT * FROM products ORDER BY price DESC ")
sorted_data = cur.fetchall()
for row in sorted_data :
    print (row)

db.commit()
db.close()