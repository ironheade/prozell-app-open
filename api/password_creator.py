# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:51:31 2022

@author: bendzuck
"""


import string
import random
import sqlite3
import os
import json
import pandas as pd




## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
user_characters = list(string.ascii_letters)

def generate_random_password(length):
	random.shuffle(characters)

	password = []
	for i in range(length):
		password.append(random.choice(characters))

	random.shuffle(password)

	return("".join(password))
    
def generate_random_user(length):
	random.shuffle(user_characters)

	username = []
    
	for i in range(length):
		username.append(random.choice(user_characters))

	random.shuffle(username)

	return("".join(username))

def generate_users(amount,Startzeit,Endzeit,StartzeitMS,EndzeitMS):
    Zugangsdaten = []
    i=0
    while i < amount:
        #print("username: {}    password: {}    valid from: {}    valid until: {}".format(generate_random_user(10),generate_random_password(20),datetime.datetime.now().date(),datetime.datetime.now().date()))
        
        
        db = sqlite3.connect(os.path.abspath("passwort.db"))
        cursor = db.cursor()
    
        Nutzer = generate_random_user(10)
        Passwort = generate_random_password(20)
        
        query_data = [Nutzer,Passwort,Startzeit,Endzeit,StartzeitMS,EndzeitMS]
        sqlite_insert_query = """INSERT INTO Zugangsdaten
                          (Nutzername,Passwort,Startzeit,Endzeit,StartzeitMS,EndzeitMS) 
                           VALUES 
                          (?,?,?,?,?,?)"""
        cursor.execute(sqlite_insert_query,query_data)
        db.commit()
        db.close()
        
        Zugangsdaten.append({"Nutzer": Nutzer, "Passwort": Passwort, "Startzeit": Startzeit, "Endzeit":Endzeit,"StartzeitMS":StartzeitMS,"EndzeitMS":EndzeitMS})
        
        i+=1
    return(json.dumps(Zugangsdaten))

def user_check(user,password):
    db = sqlite3.connect(os.path.abspath("passwort.db"))   
    df = pd.read_sql_query('''SELECT * FROM Zugangsdaten''', db)
    db.commit()
    db.close()

    if user not in list(df["Nutzername"]):
        return 
    elif list(df.loc[df["Nutzername"]==user]["Passwort"])[0] != password:
        return
    else:
        Startzeit = list((df.loc[df["Nutzername"]==user]["Startzeit"]))[0]
        Endzeit = list((df.loc[df["Nutzername"]==user]["Endzeit"]))[0]
        StartzeitMS = list((df.loc[df["Nutzername"]==user]["StartzeitMS"]))[0]
        EndzeitMS = list((df.loc[df["Nutzername"]==user]["EndzeitMS"]))[0]
        Berechtigung = list((df.loc[df["Nutzername"]==user]["Berechtigung"]))[0]
        return json.dumps({"Startzeit":Startzeit,
                           "Endzeit":Endzeit,
                           "StartzeitMS":StartzeitMS,
                           "EndzeitMS":EndzeitMS,
                           "Berechtigung":Berechtigung
                           })

    
