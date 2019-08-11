import sqlite3


connection=sqlite3.connect('data.db')
cursor=connection.cursor()

create_table="CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

insert_row="INSERT INTO users VALUES (?,?,?)"
user=(1,'chai','fuck')
cursor.execute(insert_row,user)
users_list=[
    (2,'chaitu','haha'),
    (3,'chinni','haaa')
]
cursor.executemany(insert_row,users_list)

select_rows="SELECT * FROM users"

for row in cursor.execute(select_rows):
    print(row)
connection.commit()
connection.close()
