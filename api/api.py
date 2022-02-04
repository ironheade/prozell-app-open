import time
from flask import Flask, request
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())}

@app.route('/Zellformate')
def get_Zellformate():
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    df = pd.read_sql_query('''SELECT * FROM Zellformate''', db)

    Zellformate = df.to_json(orient='records')
    db.commit()
    db.close()
    
    return {'Zellformate': Zellformate}

#@app.route('/Zellchemien')
#def get_Zellchemien():
#    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
#    df = pd.read_sql_query('''SELECT * FROM Zellchemien''', db)
#
#    Zellchemien = df.to_json(orient='records')
#    db.commit()
#    db.close()
#    
#    return {'Zellchemien': Zellchemien}

#@app.route('/Zellchemiewahl',methods=['POST'])
#def get_Zellchemiewahl():
#    Dateiname = request.get_json()["Zellchemiewahl"]
#    
#    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
#    read_order = ('''SELECT * FROM {Dateiname}''')
#    read_order = read_order.format(Dateiname=Dateiname)
#    df = pd.read_sql_query(read_order, db)
#
#    Zellchemie = df.to_json(orient='records')
#    db.commit()
#    db.close()
#
#    return {'Zellchemie': Zellchemie}

@app.route('/tabelle_abrufen',methods=['POST'])
def get_tabelle():
    Dateiname = request.get_json()["tabelle"]
    
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    read_order = ('''SELECT * FROM {Dateiname}''')
    read_order = read_order.format(Dateiname=Dateiname)
    df = pd.read_sql_query(read_order, db)
    
    tabelle = df.to_json(orient='records')
    db.commit()
    db.close()
    
    return {'tabelle':tabelle}

#@app.route('/Zellmaterialien')
#def get_Zellmaterialien():
#    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
#    df = pd.read_sql_query('''SELECT * FROM materialien''', db)
#
#    Zellmaterialien = df.to_json(orient='records')
#    db.commit()
#    db.close()
#    
#    return {'Zellmaterialien': Zellmaterialien}

@app.route('/Zellwahl',methods=['POST'])
def get_Zellwahl():
    Dateiname = request.get_json()["Zelle"]
    
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    read_order = ('''SELECT * FROM {Dateiname}''')
    read_order = read_order.format(Dateiname=Dateiname)
    df = pd.read_sql_query(read_order, db)

    Zellinfo = df.to_json(orient='records')
    db.commit()
    db.close()

    return {'Zellinfo': Zellinfo}