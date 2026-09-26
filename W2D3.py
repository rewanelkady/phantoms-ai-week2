from flask import Flask, json, request
import sqlite3

app = Flask(__name__)

def init_db():
  db = sqlite3.connect("store.db")
  cur = db.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS webhook1a_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
  db.commit()
  db.close()

init_db()

@app.route("/webhook",methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    print ("Server is up and running")

    if data is not None:
        json_string = json.dumps(data, ensure_ascii=False)

        db = sqlite3.connect("store.db")
        cur = db.cursor()
        cur.execute(
            "INSERT INTO webhook1a_logs (received_data) VALUES (?)", (json_string,)
        )
        db.commit()
        db.close()
        print("Data saved to database successfully!")
        return {"status": "success"},200

if __name__ == "__main__":
  app.run(debug=True, port=5000)