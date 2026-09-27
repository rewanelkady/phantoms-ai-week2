import sqlite3
import time
import requests

API_KEY = "3db4c7ea05375f1ddd5efbfb23bfe7c"
API_URL = f"https://api.openweathermap.org/data/2.5/weather?q=Cairo&appid={API_KEY}&units=metric"
WEBHOOK_URL = "http://127.0.0.1:5000/webhook"


def setup_database():
  conn = sqlite3.connect("store.db")
  cursor = conn.cursor()
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
  )
  conn.commit()
  conn.close()


def run_pipeline(cycle_number):
  print(f"\n--- Cycle {cycle_number} Started ---")
  try:
    print("1. Fetching data from API...")
    response = requests.get(API_URL)
    if response.status_code != 200:
      print(f"Request failed! Status code: {response.status_code}")
      return

    data = response.json()
    city = data.get("name")
    temp = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]

    print("2. Storing data into database (store.db)...")
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO weather_logs (city, temperature, description)
            VALUES (?, ?, ?)
        """,
        (city, temp, weather_desc),
    )
    conn.commit()
    conn.close()

    payload = {
        "cycle": cycle_number,
        "city": city,
        "temperature": temp,
        "description": weather_desc,
    }

    print("3. Sending data to Webhook...")
    webhook_response = requests.post(WEBHOOK_URL, json=payload)
    if webhook_response.status_code == 200:
      print(f"Cycle {cycle_number} completed successfully.")
    else:
      print(f"Webhook failed. Status code: {webhook_response.status_code}")

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  setup_database()
  cycle_count = 1
  print("Automation pipeline started. Press Ctrl+C to stop.")
  try:
    while True:
      run_pipeline(cycle_count)
      cycle_count += 1
      print("Waiting 30 seconds for the next cycle...\n")
      time.sleep(30)
  except KeyboardInterrupt:
    print("\nAutomation stopped by user.")