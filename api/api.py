import time
from flask import Flask, request
import sqlite3
import pandas as pd
import os
import sys
import json
import Zellberechnung
import Kostenberechnung

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
    

    print(Kostenberechnung.Kostenberechnung())
    #print(Ergebnisse)
    Ergebnisse = Kostenberechnung.Kostenberechnung()
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
    
    # #Die Zellchemie abrufen und in ein df umwandeln
    # a_json = json.loads(Zellchemie)
    # dfItem = pd.DataFrame.from_records(a_json)
    # print(dfItem, file=sys.stderr)

    # #Die Materialinfos abrufen und in ein df umwandeln
    # b_json = json.loads(Materialinfos)
    # complete_df = []
    # for Material_tabelle in b_json:
    #     Material = list(Material_tabelle.keys())[0]
    #     for Spalte in Material_tabelle[Material]:
    #         Spalte["Material"]=Material
    #         complete_df.append(Spalte)
    # print(pd.DataFrame.from_records(complete_df))

    # d_json = json.loads(zellformat)
    # print(pd.DataFrame.from_records(d_json))
    
    # e_json = json.loads(zellformatName)
    # df = pd.DataFrame.from_dict(e_json, orient="index")
    # print(df)

    Zellergebnisse = Zellberechnung.zellberechnung(Zellchemie, Materialinfos, zellformat, zellformatName, GWh_Jahr_Ah_Zelle)
    print(Zellergebnisse)
    Zellergebnisse = Zellergebnisse.to_json(orient='records')
    
    return {'Zellergebnisse': Zellergebnisse}


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