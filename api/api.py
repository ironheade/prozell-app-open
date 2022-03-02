import time
from flask import Flask, request
import sqlite3
import pandas as pd
import os
import sys
import json
import Zellberechnung
import Kostenberechnung
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
#cors = CORS(app, resources={
#    r"/*": {
#        "origins":"*"
#    }
#})

@app.route('/')
def greetings():
    return """<h1><a  href="https://i.gifer.com/1Ms.gif">Buenas noches, amigo!</a></h1>"""
    #return ("Hello World")

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

@app.route('/Ergebnisse', methods=['POST'])
def get_ergebnisse():

    Zellergebnisse = request.get_json()["Zellergebnisse"]
    Zellchemie = request.get_json()["Zellchemie"]
    Prozessroute = request.get_json()["Prozessroute"]
    Prozessroute_array = request.get_json()["Prozessroute_array"]
    Prozessdetails = request.get_json()["Prozessdetails"]
    Materialinfos = request.get_json()["Materialinfos"]
    Oekonomische_parameter = request.get_json()["Oekonomische_parameter"]
    Mitarbeiter_Logistik = request.get_json()["Mitarbeiter_Logistik"] 
    Gebaeude = request.get_json()["Gebaeude"] 
    
    #Zellergebnisse = pd.DataFrame.from_records(json.loads(Zellergebnisse))
    
    #print("Zellergebnisse")
    #print(Zellergebnisse)
    #print("Prozessroute_array")
    #print(Prozessroute_array)
    #print("Prozessroute")
    #print(Prozessroute)
    #print("Prozessdetails")
    #print(Prozessdetails)
    #print("Materialinfos")
    #print(Materialinfos)
    #print("Oekonomische Parameter")
    #print(Oekonomische_parameter)
    #print("Mitarbeiter und Logistik")
    #print(Mitarbeiter_Logistik)
    #print("Gebäude")
    #print(Gebaeude)
    

    #print(Kostenberechnung.Kostenberechnung())
    #print(Ergebnisse)
    Ergebnisse = Kostenberechnung.Kostenberechnung(
        Zellergebnisse,
        Zellchemie,
        Prozessroute_array,
        Prozessdetails,
        Materialinfos,
        Oekonomische_parameter,
        Mitarbeiter_Logistik,
        Gebaeude
    )
    Ergebnisse = Ergebnisse.to_json(orient="records")
    return {'Ergebnisse': Ergebnisse}

@app.route('/Zellergebnisse', methods=['POST'])
def get_zellergebnisse():
    Zellchemie = request.get_json()["Zellchemie"]
    Materialinfos = request.get_json()["Materialinfos"]
    zellformat = request.get_json()["zellformat"]
    zellformatName = request.get_json()["zellformatName"]
    GWh_Jahr_Ah_Zelle = request.get_json()["GWh_Jahr_Ah_Zelle"]
    
    print("Zellchemie")
    print(Zellchemie)
    print("Materialinfos")
    print(Materialinfos)
    print("zellformat")
    print(zellformat)
    print("zellformatName")
    print(zellformatName)
    print("GWh_Jahr_Ah_Zelle")
    print(GWh_Jahr_Ah_Zelle)
    
    a_json = json.loads(GWh_Jahr_Ah_Zelle)
    print(a_json["GWh_pro_jahr"])

 
    Zellergebnisse = Zellberechnung.zellberechnung(Zellchemie, Materialinfos, zellformat, zellformatName, GWh_Jahr_Ah_Zelle)
    print(Zellergebnisse)
    Zellergebnisse = Zellergebnisse.to_json(orient='records')
    
    return {'Zellergebnisse': Zellergebnisse}

