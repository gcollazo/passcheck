import os

import httpx
import psycopg2

password_file_url = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/"
    "500-worst-passwords.txt"
)

# Download the password list
print("-> Downloading password list")
r = httpx.get(password_file_url)
password_list = r.text.split("\n")[:-1]

# Insert the passwords into the database
print("-> Creating passwords table")
conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS passwords")
cur.execute(
    "CREATE TABLE IF NOT EXISTS passwords (id serial PRIMARY KEY,"
    "value varchar (255) NOT NULL)"
)

print("-> Inserting passwords into database")
for p in password_list:
    cur.execute("INSERT INTO passwords (value) VALUES (%s)", (p,))

conn.commit()
cur.close()
conn.close()

print("-> Done!")
