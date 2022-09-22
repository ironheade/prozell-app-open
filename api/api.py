import time
from flask import Flask, request
import sqlite3
import pandas as pd
import os
import json
import Zellberechnung
import Kostenberechnung
from password_creator import generate_users , user_check
from flask_cors import CORS
from update_db import update_table
#import locale


app = Flask(__name__)
CORS(app)

@app.route('/')
def greetings():
    return """<h1><a  href="https://i.gifer.com/1Ms.gif">Buenas noches, amigo!</a></h1>"""

@app.route('/time')
def get_current_time():
    return {'time': time.strftime("%a, %d %b %Y %H:%M:%S")}

@app.route('/all_tables')
def get_all_tables():
    db = sqlite3.connect(os.path.abspath("Datenbank.db"))
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    db.commit()
    db.close()
    
    return {'tables': tables}

@app.route('/update_db',methods=['POST'])
def update_db():
    new_table = request.get_json()["new_table"]
    new_table_name = request.get_json()["new_table_name"]
    update_table(new_table,new_table_name)

    return "None"

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

@app.route('/Nutzer_abrufen',methods=['POST'])
def get_Nutzer():
    Dateiname = request.get_json()["Zugangsdaten"]

    db = sqlite3.connect(os.path.abspath("passwort.db"))
    read_order = ('''SELECT * FROM {Dateiname}''')
    read_order = read_order.format(Dateiname=Dateiname)
    df = pd.read_sql_query(read_order, db)
        
    tabelle = df.to_json(orient='records')
    db.commit()
    db.close()
        
    return tabelle


@app.route('/user_check',methods=['POST'])
def check_user():
    Nutzer = request.get_json()["Nutzer"]
    Passwort = request.get_json()["Passwort"]    
    check = user_check(Nutzer,Passwort)
    print(check)
    if check == None:
        return "false"
    else:
        return check
    

@app.route('/nutzer_generieren',methods=['POST'])
def nutzer_generieren():
    Anzahl = request.get_json()["Anzahl"]
    Startzeit = request.get_json()["Startzeit"]
    Endzeit = request.get_json()["Endzeit"]
    StartzeitMS = request.get_json()["StartzeitMS"]
    EndzeitMS = request.get_json()["EndzeitMS"]
    Kommentar = request.get_json()["Kommentar"]

    Nutzer = generate_users(Anzahl,Startzeit,Endzeit,StartzeitMS,EndzeitMS,Kommentar)
    return Nutzer

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
    GWh_Jahr_Ah_Zelle = request.get_json()["GWh_Jahr_Ah_Zelle"]
    
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
    Rechenrgebnisse = Kostenberechnung.Kostenberechnung(
        Zellergebnisse,
        Zellchemie,
        Prozessroute_array,
        Prozessdetails,
        Materialinfos,
        Oekonomische_parameter,
        Mitarbeiter_Logistik,
        Gebaeude,
        GWh_Jahr_Ah_Zelle
    )
    Ergebnisse = Rechenrgebnisse[0].to_json(orient="records") #df to json
    Materialkosten = json.dumps(Rechenrgebnisse[1]) #dict to json
    Rückgewinnung = json.dumps(Rechenrgebnisse[2]) #dict to json 
    Baukosten = json.dumps(Rechenrgebnisse[3]) #dict to json 
    Flächenverteilung = json.dumps(Rechenrgebnisse[4]) #dict to json
    levelized_cost_total = json.dumps(Rechenrgebnisse[5]) #dict to json
    overhead_kosten = json.dumps(Rechenrgebnisse[6]) #dict to json

    return {'Ergebnisse': Ergebnisse,
            'Materialkosten':Materialkosten,
            'Rückgewinnung':Rückgewinnung,
            'Baukosten':Baukosten,
            'Flächenverteilung':Flächenverteilung,
            'levelized_cost_total':levelized_cost_total,
            'overhead_kosten':overhead_kosten
            }

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

