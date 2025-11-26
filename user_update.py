import sqlite3

# This script goes through the users in the users table and gives them an entry in the preference table.
# It is not needed for the webapp, as an entry in the preference table will be created upon registration now. 
# It was just used to give entries for the test users I created before the preference table existed.
# I'm keeping it here in case I ever need it again.

with sqlite3.connect('data.db') as con:
    cur = con.cursor()

cur.execute(''' INSERT INTO preference (user_id)
                SELECT id
                FROM users''')
con.commit()
cur.close()