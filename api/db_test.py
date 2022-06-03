# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:24:52 2022

@author: bendzuck
"""



import sqlite3
import os
import json


db = sqlite3.connect(os.path.abspath("Datenbank.db"))
cursor = db.cursor()

query = 'Select COLUMNS FROM assemblieren'
#print(cursor.execute(query))

def update_row(table_name,Wert,id_nr):
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    cursor = db.cursor()
    #cursor.execute("SELECT * FROM {}".format("aa_test_table"))
    #cursor.execute('INSERT INTO aa_test_table VALUES (?,?,?,?)',(29,"Zeil7e29", 555, "mm"))
    
    query = 'UPDATE {} SET Wert = {} WHERE id={}'.format(table_name,Wert,id_nr)
    cursor.execute(query)
    
    db.commit()
    cursor.close()
    
    db.close()


def update_table(JSONdata,table_name):
    for row in JSONdata:
        update_row(table_name,row["Wert"],row["id"])
        
#update_table(tabelle)
        
def do_query(query):
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    cursor = db.cursor()
    c = cursor.execute(query)
    for row in c:
        Chemien.append(row[0])
    db.commit()
    db.close()

Chemien = []
query_1 = "SELECT Dateiname FROM Zellchemien"
do_query(query_1)
print(Chemien)


# for Chemie in Chemien:
#     query = "ALTER TABLE {} rename to {}".format(Chemie,"zellchemie_"+Chemie)
#     do_query(query)
#INTEGER PRIMARY KEY AUTO_INCREMENT=1
new_query = 'ALTER TABLE "material_NCM_111" ALTER COLUMN id INTEGER NOT NULL'
do_query(new_query)