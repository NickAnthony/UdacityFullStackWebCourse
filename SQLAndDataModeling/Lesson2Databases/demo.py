import psycopg2

conn = psycopg2.connect('dbname=example')

cursor = conn.cursor()

# drop any existing todos table
cursor.execute("DROP TABLE IF EXISTS todos;")

cursor.execute("""
  CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
""")

cursor.execute("INSERT INTO todos (id, completed) VALUES (%(id)s, %(completed)s);",{
    "id": 1,
    "completed": True
})
cursor.execute("INSERT INTO todos (id, completed) VALUES (%(id)s, %(completed)s);",{
    "id": 2,
    "completed": True
})

# commit, so it does the executions on the db and persists in the db
conn.commit()


cursor.execute("SELECT * FROM todos;")

result1 = cursor.fetchone()
new_result = (result1[0], not result1[1])

cursor.execute("UPDATE todos SET completed=%(completed)s WHERE id=%(id)s;", {
    "completed": new_result[1],
    "id": new_result[0],
})
conn.commit()

print("Changed " + str(result1) + " to " + str(new_result))

cursor.execute("SELECT * FROM todos;")
results = cursor.fetchall()
for result in results:
    print("result: ", result)



cursor.close()
conn.close()
