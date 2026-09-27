import requests 
import sqlite3
import time

def run(cycle_num):

    url = "https://api.openweathermap.org/data/2.5/weather"
    par = {
        "q": "Cairo",
        "appid": "YOUR_API_KEY_HERE"
    }

    res = requests.get(url, params=par)

    if res.status_code == 200 :
        print (f"URL {url} Status Code is : {res.status_code}")
        data = res.json()
        
        db = sqlite3.connect('store.db')
        cur = db.cursor()

        cur.execute("DROP TABLE IF EXISTS products")
        cur.execute("CREATE TABLE data (city ,temp)")

        city = data.get("name")
        temp = data.get("main", {}).get("temp")
        cur.execute("INSERT INTO data VALUES(?,?)" ,(city,temp))

        db.commit()
        db.close()
        print (data)
        print ("Done connect database")


        webhook_url = "http://127.0.0.1:5000/webhook"
        
        payload = {
            "city": city,
            "temperature": temp
        }

        requests.post(webhook_url, json=payload)
        print ("Done connect webhook")
        print(f"Cycle number {cycle_num} executed successfully")
    else :
        print("Error")
        print (res.text)

if __name__ == "__main__":
    counter = 1  
    
    while True:
        run(counter)  
        counter += 1  

        time.sleep(30)