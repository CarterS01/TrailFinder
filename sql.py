#This file is just to test bcrypt and sqlite in a simpler environment before
#implementing some of these features into the full webapp.

import bcrypt
import sqlite3

pw_to_hash = [b'pass1', b'pass2', b'pass3']
pws = ['pass1', 'pass2', 'pass3']
un = ['testuser1', 'testuser2', 'testuser3']

with sqlite3.connect("data.db") as con: #add timeout=xx arg if db is locked to give thread more time to wait
                                        #for current thread to release control on db before giving up.
    cur = con.cursor()

j=0
for i in pw_to_hash:
    hashed = bcrypt.hashpw(i, bcrypt.gensalt())
    upload = hashed.decode('utf-8')

    user = un[j]

    cur.execute(''' UPDATE users
                    SET pw_hash=?
                    WHERE username=?''',
                    (upload, user))
    con.commit()

    j+=1

j=0
for i in pws:
    user = un[j]

    cur.execute(''' SELECT pw_hash
                    FROM users
                    WHERE username=?''',
                    (user,))
    
    password = cur.fetchall()
    res = str(password).strip('[](),\'')

    if bcrypt.checkpw(i.encode('utf-8'), res.encode('utf-8')):
        print(f'Successfully matched password {j+1}')

    j+=1

cur.close()