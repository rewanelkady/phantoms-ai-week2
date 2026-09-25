import sqlite3
import requests

db = sqlite3.connect('store.db')
cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS products")

cur.execute("""CREATE TABLE products (
            user_id INTEGER,
            product_id INTEGER,
            title TEXT)""")

url = "https://jsonplaceholder.typicode.com/posts"
res = requests.get(url)
print("Status Code:", res.status_code)

if res.status_code == 200:
    posts = res.json()
    
    for post in posts[:5]:
        u_id = post.get("userId")
        p_id = post.get("id")
        p_title = post.get("title")
        
        cur.execute("INSERT INTO products (user_id, product_id, title) VALUES (?, ?, ?)", (u_id, p_id, p_title))

cur.execute("SELECT * FROM products WHERE user_id = 1")
electronics_data = cur.fetchall()
for row in electronics_data:
    print(row)


cur.execute("SELECT * FROM products ORDER BY product_id DESC")
sorted_data = cur.fetchall()
for row in sorted_data :
    print (row)

db.commit()
db.close()