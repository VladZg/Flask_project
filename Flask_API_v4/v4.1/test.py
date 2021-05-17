# import sqlite3
#
# connection = sqlite3.connect('data.db')
# cursor = connection.cursor()

# create_user = 'INSERT INTO users VALUES (NULL, ?, ?)'
# users = [
#     ('anatolii', '123'),
#     ('masha', '456'),
#     ('dasha', 'qwe')
# ]
# cursor.executemany(create_user, users)

# for row in cursor.execute('SELECT * FROM users'):
#     print(row)
#
# print()
#
# create_item = 'INSERT INTO store VALUES (NULL, ?, ?)'
# items = [
#     ('item1', 1500),
#     ('item2', 2000),
#     ('item3', 2500)
# ]
# cursor.executemany(create_item, items)
#
# for row in cursor.execute('SELECT * FROM store'):
#     print(row)
#
# connection.commit()
# connection.close()
