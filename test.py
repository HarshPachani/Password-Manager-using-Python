import sqlite3
conn = sqlite3.connect("passwords.db")
cur = conn.cursor()
cur.execute('SELECT * FROM pass')
data = cur.fetchall()
for d in data:
    print(d)
website = data[0][0]
email = data[0][1]
password = data[0][2]
print(website)
print(email)
print(password)