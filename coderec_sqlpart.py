import sqlite3

conn=sqlite3.connect('./database/mini.db')

#cur contains database object (in perticular cursor object)
#cur=conn.cursor()

def createtable():
    cur=conn.cursor() 
    cur.executescript(""" 
    CREATE TABLE IF NOT EXISTS Record(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date DATE,
        no_prob_solved INTEGER,
        plateform_id INTEGER 
    );
    CREATE TABLE IF NOT EXISTS  Plateform(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        plateform_name TEXT UNIQUE,
        npspp INTEGER
    );
    """)
    #no_prob_solved_per_plateform(npspp)
    conn.commit()
    cur.close()

#Function to insert data record
def data_entry():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    d,p,n=input("""Enter todays coding record : """).split()
    n=int(n)
    cur.execute("""INSERT INTO Coderecord (date,plateform,noprobsolved)
    VALUES(?,?,?)
    """,(d,p,n))
    conn.commit()
    cur.close()

#Function to insert more than one data record
def manydata_entry():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    dataset=list()
    print("Enter multiple datasets and enter 'finish' to exit and 'continue' to continue: ")
    t=tuple()
    switch=str()
    while switch !='finish':
        print('Enter data')
        t=input().split()
        dataset.append(t)
        switch=input()
    cur.executemany("""
    INSERT INTO Coderecord (date,plateform,noprobsolved)
    VALUES(?,?,?)
    """,dataset)
    conn.commit()
    conn.close()

#Function to read the data of database so far
def read_database():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    cur.execute('SELECT rowid,* FROM Coderecord ORDER BY noprobsolved DESC')
    recli=cur.fetchall()
    for rec in recli:
        print("{}\t{}\t{}\t{}".format(rec[0],rec[1],rec[2],rec[3])) 
    conn.close()

#Function to update the database
def update_databse():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    cur.execute('UPDATE Coderecord SET noprobsolved=(?) WHERE rowid=(?)',(10,2))
    conn.commit()
    conn.close()

#Function to delete a record in database
def delete_databse():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    d=int(input('Enter rowid which has to be removed : '))
    cur.execute('DELETE FROM Coderecord WHERE rowid=(?)',(d,))
    conn.commit()
    conn.close()

#Function to drop table(deletes whole table)
def delete_table():
    conn=sqlite3.connect('./database/mini.db')
    cur=conn.cursor()
    cur.execute('DROP TABLE Coderecord')
    conn.commit()
    conn.close()


createtable()
#closes the connection
conn.close()
