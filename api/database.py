import sqlite3
from sqlite3 import Error
import pandas as pd
import os
import time

#Create a Database
#_____________________________________________________
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


#create_connection("C:/Users/bendzuck/Desktop/Visual Studio/flask app/new-app/api/Datenbank.db")


def csv_to_table_new(table_name, path, exceptions):
    
    # table_name = "Formieren"
    database = "Datenbank.db"
    # path = r"C:/Users/bendzuck/Desktop/test/Prozessschritte/formieren.csv"
    # exceptions = ["Wert","Werte","Kosten"] #Werte die kein TEXT sondern REAL sind
    
    #read the csv, replace the "Unnamed" with "Beschreibung", get a list of the headers, encoding vormals 'latin-1'
    df = pd.read_csv(path,encoding='cp1252')
    df.rename(columns={'Unnamed: 4': 'empty'}, inplace=True)
    df.rename(columns={'Unnamed: 0': 'Beschreibung'}, inplace=True)
    df_header = list(df.columns.values)
      
    table_headers = ""
    for header in df_header:
        if header in exceptions:
            table_headers = table_headers+header+" REAL,"
        else:
            table_headers = table_headers+header+" TEXT,"
    table_headers = table_headers[:-1]

    
    #create the table
    create_order = '''
        CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY, {headers}
        )
    '''
    create_order = create_order.format(headers = table_headers, table_name = table_name)

    db = sqlite3.connect(os.path.abspath(database))
    cursor = db.cursor()
    print(create_order)
    cursor.execute(create_order)

    #populate the table
    order_of_entries = "("
    for header in df_header:
        order_of_entries = order_of_entries+header+","
    order_of_entries = order_of_entries[:-1]
    order_of_entries = order_of_entries+")"
    
    questionmarks = "("
    questionmarks = questionmarks + "?," * len(df_header)
    questionmarks = questionmarks[:-1]
    questionmarks = questionmarks+")"

    populate_order = '''INSERT INTO {table_name}{order_of_entries}
                      VALUES{questionmarks}'''
    populate_order = populate_order.format(table_name = table_name, order_of_entries = order_of_entries, questionmarks = questionmarks)
    
    #get tuples for each row of the df
    records = df.to_records(index=False)

    tuples = list(records)

    for tuple_ in tuples:
        cursor.execute(populate_order, tuple_)

    db.commit()
    db.close()

    
#csv_to_table_new()   
#prozessschritte_csv = os.listdir(r"C:/Users/bendzuck/Desktop/test_to_db/Prozessschritte")
    
# prozessschritte_csv = os.listdir(r"C:/Users/bendzuck/Desktop/test_to_db/Zellformate")
# prozesschritte = []
# print(prozessschritte_csv)
# for prozess in prozessschritte_csv:
#     prozesschritte.append(prozess.split(".")[0])
# print(prozesschritte)
# for num,prozess in enumerate(prozesschritte):
#     exceptions = ["Wert","Werte","Kosten"] #Werte die kein TEXT sondern REAL sind
#     path = r"C:/Users/bendzuck/Desktop/test_to_db/Zellformate/"+prozessschritte_csv[num]
#     #print(path)
#     csv_to_table_new(prozess, path, exceptions)


#Rename an entry
#_____________________________________________________
def rename_entry():
    db = sqlite3.connect(os.path.abspath('Datenbank.db'))
    
    cursor = db.cursor()
    cursor.execute('''
        UPDATE Zellformate
            SET Dateiname = ?
            WHERE id = ?
        
    ''',("PHEV_2plus_HC",9))
    db.commit()
    db.close()

#rename_entry()
#Add a table
#_____________________________________________________
def add_table():

    db = sqlite3.connect('databse.db')
    
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    db.commit()
    db.close()
    
    db = sqlite3.connect('databse.db')
    
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Zellchemien(
            id INTEGER PRIMARY KEY,
            Wert TEXT,
            Einheit REAL,
            Besonderheit TEXT
        )
    ''')
    db.commit()
    db.close()

#Populate a Table
#_____________________________________________________
def populate_table():
    db = sqlite3.connect('databse.db')
    
    cursor = db.cursor()
    name = 'Manny'
    phone = '23456565'
    email = 'Manny@example.com'
    password = '12345'
    cursor.execute('''INSERT INTO users(name, phone, email, password)
                      VALUES(?,?,?,?)''', (name,phone, email, password))
    db.commit()
    db.close()




#Liste eintragen in Datenbank
#_____________________________________________________
def list_to_db():
    path = r"C:/Users/bendzuck/Desktop/test/Zellformate"
    liste = os.listdir(path)
    liste2 = []
    for eintrag in liste:
        liste2.append(eintrag.split(".")[0])
    print(liste)
    print(liste2)
    
    db = sqlite3.connect('database.db')
    
    cursor = db.cursor()
    for eintrag in liste2:
        Format = eintrag
        cursor.execute('''INSERT INTO Zellformate(Format)
                          VALUES(?)''', (Format,))
        db.commit()
    
    db.close()


def get_Zellformate():
    #db = sqlite3.connect('C:/Users/bendzuck/Desktop/Visual Studio/flask app/new-app/api/database.db')
    db = sqlite3.connect(os.path.abspath('database.db'))
    df = pd.read_sql_query('''SELECT * FROM Zellformate''', db)

    Zellformate = df.to_json(orient='records')
    db.commit()
    db.close()
    
    return {'Zellformate': Zellformate}



def get_current_data():
    df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
    'physics': [28, 74, 77, 78],
    'chemistry': [84, 56, 73, 69],
    'algebra': [78, 88, 82, 87]})

    json = df_marks.to_json(orient='records')

    return {'json_data': json}


def get_current_time():
    print("blabla")
    return {'tome': time.time()}


#Read a Table
#_____________________________________________________
def read_table():
    db = sqlite3.connect('database.db')
    #cursor = db.cursor()
    # cursor.execute('''SELECT * FROM Zellformate''')
    # user1 = cursor.fetchall() #retrieve the first row
    # print (user1)
    
    df = pd.read_sql_query('''SELECT * FROM Zellformate''', db)
    print(df)
    df = df.to_json(orient="records")
    print(df)
    db.commit()
    db.close()



# #print(user1[0])
# all_rows = cursor.fetchall()
# for row in all_rows:
#     # row[0] returns the first column in the query (name), row[1] returns email column.
#     print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
# # The cursor object works as an iterator, invoking fetchall() automatically:
# cursor.execute('''SELECT name, email, phone FROM users''')
# for row in cursor:
#     print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))

# # To retrive data with conditions, use again the "?" placeholder:
# user_id = 3
# cursor.execute('''SELECT name, email, phone FROM users WHERE id=?''', (user_id,))
# user = cursor.fetchone()
# db.commit()
# db.close()


#Delete a  table
#_____________________________________________________
def delete_table():
    db = sqlite3.connect('databse.db')
    
    cursor = db.cursor()
    cursor.execute('DROP TABLE users')
    db.commit()
    db.close()

#Add a csv to Database
#_____________________________________________________
def csv_to_table():
    db = sqlite3.connect('databse.db')
    #cursor = db.cursor()
    
    df = pd.read_csv(r"C:/Users/bendzuck/Desktop/test/allgemeine_parameter/gebaeude_trockenraum.csv",encoding='latin-1')
    df.rename(columns={'Unnamed: 0': 'Beschreibung'}, inplace=True)
    print(df)
    df.to_sql("Gebäude und Trockenraum", db, if_exists="replace")
    
    db.commit()
    db.close()


#populate the Database with all process steps
#_____________________________________________________
def folder_entries_to_table():
    path = r"C:/Users/bendzuck/Desktop/test/Zellformate"
    liste = os.listdir(path)
    liste2 = []
    for eintrag in liste:
        liste2.append(eintrag.split(".")[0])
    print(liste)
    print(liste2)
    
    db = sqlite3.connect('database.db')
    for num,eintrag in enumerate(liste2):
        csv_name = liste[num]
        df = pd.read_csv(path+"/"+csv_name,encoding='latin-1')
        df.rename(columns={'Unnamed: 0': 'Beschreibung'}, inplace=True)
        df.to_sql(eintrag, db, if_exists="replace",index=True, index_label='id')
        print(num)
        print(eintrag)
    
    db.commit()
    db.close()



# import pandas as pd
# df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
# 'physics': [28, 74, 77, 78],
# 'chemistry': [84, 56, 73, 69],
# 'algebra': [78, 88, 82, 87]})

# json = df_marks.to_json(orient='records')
# print(json)



def get_Zellformate():
    db = sqlite3.connect('C:/Users/bendzuck/Desktop/Visual Studio/flask app/new-app/api/database.db')
    df = pd.read_sql_query('''SELECT * FROM Zellformate''', db)

    Zellformate = df.to_json(orient='records')
    db.commit()
    db.close()
    
    return {'Zellformate': Zellformate}