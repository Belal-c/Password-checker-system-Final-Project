import sqlite3
import os
import requests

DB_NAME = "weak_passwords.db"
FLAG = "db_ready.flag"


URL = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"


def download_file():
    print("Downloading password file...")

    response = requests.get(URL, stream=True)
    with open("rockyou.txt", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Download completed")


def init_db():

   
    if os.path.exists(FLAG):
        print("DB already exists")
        return

   
    download_file()

    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weak_passwords (
            password TEXT UNIQUE
        )
    """)

   
    batch = []

    with open("rockyou.txt", "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            password = line.strip()

            if password:
                batch.append((password,))

           
            if len(batch) == 1000:
                cursor.executemany(
                    "INSERT OR IGNORE INTO weak_passwords(password) VALUES (?)",
                    batch
                )
                conn.commit()
                batch.clear()

   
    if batch:
        cursor.executemany(
            "INSERT OR IGNORE INTO weak_passwords(password) VALUES (?)",
            batch
        )
        conn.commit()

    conn.close()

   
    os.remove("rockyou.txt")

    with open(FLAG, "w") as f:
        f.write("done")

    print("Database created successfully")


if __name__ == "__main__":
    init_db()