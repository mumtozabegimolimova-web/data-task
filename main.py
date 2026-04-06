import json
import re
import psycopg2

with open("task1_d.json", "r", encoding="utf-8") as f:
    data = f.read()

data = data.replace("=>", ":")
data = data.replace("€", "")

data = data.replace("{:", "{")
data = data.replace(", :", ", ")

data = re.sub(r'([{,])\s*(\w+):', r'\1 "\2":', data)

print("Первые 200 символов:")
print(data[:200])

parsed = json.loads(data)

print("Загружено записей:", len(parsed))


conn = psycopg2.connect(
    dbname="books_db",
    user="postgres",
    password="162825",  
    host="localhost",
    port="5432"
)

cur = conn.cursor()

for item in parsed:
    cur.execute("""
        INSERT INTO books (id, title, author, genre, publisher, publication_year, price, currency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        item.get("id"),
        item.get("title"),
        item.get("author"),
        item.get("genre"),
        item.get("publisher"),
        item.get("year"),
        float(item.get("price", 0).replace("$", "")),
        "EUR"
    ))

conn.commit()

cur.execute("SELECT COUNT(*) FROM books")
print("Записей в базе:", cur.fetchone()[0])

cur.close()
conn.close()