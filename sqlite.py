import sqlite3

connection=sqlite3.connect('studentdb.db')

cursor=connection.cursor()

table_info="""
CREATE TABLE IF NOT EXISTS students(NAME VARCHAR(20),CLASS VARCHAR(20),
AGE INT);
"""

cursor.execute(table_info)

cursor.execute('''INSERT INTO students VALUES("John","10th",15)''')
cursor.execute('''INSERT INTO students VALUES("Alice","9th",14)''')
cursor.execute('''INSERT INTO students VALUES("Bob","11th",16)''')  
cursor.execute('''INSERT INTO students VALUES("Eve","10th",15)''')
cursor.execute('''INSERT INTO students VALUES("Charlie","9th",14)''')

print("Data inserted are:")
data=cursor.execute('''SELECT * FROM students''')
for row in data:
    print(row)
    

connection.commit()
connection.close()  