import sqlite3

conn=sqlite3.connect('databasefile.db')

#cur contains database object (in perticular cursor object)
#cur=conn.cursor()

def createtable():
    cur=conn.cursor() 
    cur.executescript(""" 
    CREATE TABLE IF NOT EXISTS Record(
        no_prob_solved INTEGER,
        plateform_id INTEGER NOT NULL,
        trackdate_id INTEGER NOT NULL,
        PRIMARY KEY (plateform_id,trackdate_id) 
    );
    CREATE TABLE IF NOT EXISTS  Plateform(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        plateform_name TEXT UNIQUE,
        npspp INTEGER
    );
    CREATE TABLE IF NOT EXISTS Trackdate(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date TEXT,
        tpd INTEGER
    )
    """)

    # total number of problems solved that day (tnpstd->tpd)
    #no_prob_solved_per_plateform(npspp)
    conn.commit()
    cur.close()

def get_foreign_key(table_name,attribute,attribute_match):
    cur=conn.cursor()
    #getting foreign key
    cur.execute(""" 
    SELECT * FROM (?) WHERE (?)=(?)
    """,(table_name,attribute,attribute_match))
    li=cur.fetchall()
    return li[0][0]


#Function to insert data record
def data_entry(date,no_prob_solved,plateform):
    cur=conn.cursor()
    no_prob_solved=int(no_prob_solved)
    #First insert to plateform table
    cur.execute('SELECT * FROM Plateform WHERE plateform_name=(?)',(plateform,))
    li=cur.fetchall()
    #there is no row which has current plateform name (its new and i have to insert) 

    if len(li)==0:
        cur.execute("""INSERT INTO Plateform (plateform_name,npspp)
        VALUES (?,?)""",(plateform,no_prob_solved))
    else:
        #there exist a row with that perticular plateform name (i have to update)
        no_probs_done_on_plateform=li[0][2]
        cur.execute("""UPDATE Plateform SET npspp=(?) WHERE plateform_name=(?)""",(no_probs_done_on_plateform+no_prob_solved,plateform))

    #HERE WE CAN CREATE FUNCTION FOR INSERT OR UPDATE COMMAND(OPPORTUNITY TO MODULERISE THE CODE)    TODO-1

    #inserting in Track table
    cur.execute('SELECT * FROM Trackdate WHERE date=(?)',(date,))
    li=cur.fetchall()

    if len(li)==0:
        cur.execute(""" INSERT INTO Trackdate (date,tpd)
        VALUES(?,?)""",(date,no_prob_solved))
    else:
        no_prob_solved_per_day=li[0][2]
        cur.execute("""UPDATE Trackdate SET tpd=(?) WHERE date=(?)""",(no_prob_solved_per_day+no_prob_solved,date))


    #getting foriegn key
    cur.execute("""SELECT * FROM Plateform WHERE plateform_name=(?)""",(plateform,))
    li=cur.fetchall()
    plateform_id=li[0][0]
    #plateform_id=get_foreign_key('Plateform','plateform_name',plateform)
    #trackdate_id=get_foreign_key('Trackdate','date',date)
    cur.execute("""SELECT * FROM Trackdate WHERE date=(?)""",(date,))
    li=cur.fetchall()
    trackdate_id=li[0][0]

    print('plate form id : ',plateform_id,'\n','trackdate id : ',trackdate_id,)
    # insertin in record table
    cur.execute('SELECT * FROM Record WHERE plateform_id=(?) AND trackdate_id=(?)',(plateform_id,trackdate_id))
    li=cur.fetchall()
    print(li,'\n')
    if len(li)==0:
        cur.execute("""INSERT INTO Record (no_prob_solved,plateform_id,trackdate_id)
        VALUES(?,?,?)""",(no_prob_solved,plateform_id,trackdate_id))
    else:
        no_prob_solved_per_plateform=li[0][0]
        cur.execute("""UPDATE Record SET no_prob_solved=(?) WHERE plateform_id=(?) AND trackdate_id=(?)
        """,(no_prob_solved_per_plateform+no_prob_solved,plateform_id,trackdate_id))

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
data_entry('2020-6-18',5,'codechef')
data_entry('2020-6-18',3,'codeforce')
data_entry('2020-6-18',1,'hackerrank')
data_entry('2020-6-18',4,'codeforce')
data_entry('2020-6-19',11,'codeforce')
data_entry('2020-8-21',5,'hackerrank')
#closes the connection
conn.close()
