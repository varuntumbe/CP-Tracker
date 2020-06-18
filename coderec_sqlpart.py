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


    #getting foriegn key                      TODO-2 making get_foreignkey function
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





#Function to read the data of database so far
def read_database(date):
    cur=conn.cursor()
    cur.execute(""" SELECT date,no_prob_solved,plateform_name FROM Trackdate
JOIN Record JOIN Plateform on Trackdate.id=trackdate_id AND date=(?)
AND Plateform.id=plateform_id""",(date,))
    li=cur.fetchall()
    if len(li)==0:
        print('You havent done a single problem that day!!')
    else:
        t_number_prob=0
        for el in li:
            print('{}\t{}\t{}'.format(el[0],el[1],el[2]))
            t_number_prob+=el[1]
        print('Total number of problems solved : ',t_number_prob)
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
# data_entry('2020-6-18',5,'codechef')
# data_entry('2020-6-18',3,'codeforce')
# data_entry('2020-6-18',1,'hackerrank')
# data_entry('2020-6-18',4,'codeforce')
# data_entry('2020-6-19',11,'codeforce')
# data_entry('2020-8-21',5,'hackerrank')
read_database('2020-6-18')
#closes the connection
conn.close()
