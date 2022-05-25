# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:56:29 2022

@author: bendzuck
"""


import sqlite3
import os

def update_row(table_name,Wert,id_nr,columns):
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    cursor = db.cursor()
            
    for column in columns:
        
        query = 'UPDATE {} SET {} = "{}" WHERE id={}'.format(table_name,column,Wert[column],id_nr)
        #query = 'UPDATE assemblieren SET Beschreibung = Personal Facharbeiter WHERE id=1'
        cursor.execute(query)
        db.commit()
    
    cursor.close()
    db.close()


def update_table(JSONdata,table_name):
    columns = list(JSONdata[0].keys())

    for row in JSONdata:
        update_row(table_name,row,row["id"],columns)
        
