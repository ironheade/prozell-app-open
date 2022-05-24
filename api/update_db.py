# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:56:29 2022

@author: bendzuck
"""


import sqlite3
import os
import json


#tabelle =  [{"id":1,"Beschreibung":"Zeile1","Wert":100,"Einheit":"mm"},
#            {"id":2,"Beschreibung":"Zeile2","Wert":0.4,"Einheit":"mm"},
#            {"id":3,"Beschreibung":"Zeile3","Wert":45,"Einheit":"mm"},
#            {"id":4,"Beschreibung":"Zeile4","Wert":5,"Einheit":"mm"}]

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