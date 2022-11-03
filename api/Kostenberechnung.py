# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 18:06:34 2022

@author: bendzuck
"""
import pandas as pd
import json
import math
import ast
import Prozessfunktionen
from Flaechenberechnung import flaechenberechnung
from levelized_cost_calculation import levelized_cost

def Kostenberechnung(Zellergebnisse_raw,
                     Zellchemie_raw,
                     Prozessroute_array_raw,
                     Prozessdetails_raw,
                     Materialinfos_raw,
                     Oekonomische_Parameter_raw,
                     Mitarbeiter_und_Logistik_raw,
                     Gebaeude_raw,
                     GWh_Jahr_Ah_Zelle_raw):
   
    print(Prozessroute_array_raw)
    #____________________________________
    #Allgemeine Funktionen
    
    #Sucht das DF zu einem Prozessschritt raus
    def read_prozessInfo(Prozess):
        df = Prozessdetails.loc[Prozessdetails["Prozess"] == Prozess]
        return df
    
    def read_materialinfo(Material):
        df = Materialinfos.loc[Materialinfos["Material"] == Material]
        return df
    
    #____________________________________
    #parsen der Eingangsparameter in pandas df
    Zellergebnisse = pd.DataFrame.from_records(json.loads(Zellergebnisse_raw))
    Zellergebnisse = Zellergebnisse.set_index('Beschreibung')
    
    Zellchemie = pd.DataFrame.from_records(json.loads(Zellchemie_raw)) 
    Zellchemie = Zellchemie.set_index('Beschreibung')
        
    #Prozessroute_array = ast.literal_eval(Prozessroute_array_raw2)
    
    b_json = json.loads(Materialinfos_raw)
    complete_df = []
    for Material_tabelle in b_json:
        Material = list(Material_tabelle.keys())[0]
        for Spalte in Material_tabelle[Material]:
            Spalte["Material"]=Material
            complete_df.append(Spalte)
    Materialinfos = pd.DataFrame.from_records(complete_df)
    Materialinfos = Materialinfos.set_index('Beschreibung')
        
    b_json = json.loads(Prozessdetails_raw)
    complete_df = []
    for Prozess_tabelle in b_json:
        Prozess = list(Prozess_tabelle.keys())[0]
        for Spalte in Prozess_tabelle[Prozess]:
            Spalte["Prozess"]=Prozess
            complete_df.append(Spalte)
    Prozessdetails = pd.DataFrame.from_records(complete_df)
    Prozessdetails = Prozessdetails.set_index('Beschreibung')
    
    Oekonomische_Parameter = pd.DataFrame.from_records(json.loads(Oekonomische_Parameter_raw))
    Oekonomische_Parameter = Oekonomische_Parameter.set_index('Beschreibung')
    
    Mitarbeiter_und_Logistik = pd.DataFrame.from_records(json.loads(Mitarbeiter_und_Logistik_raw))
    Mitarbeiter_und_Logistik = Mitarbeiter_und_Logistik.set_index('Beschreibung')
    
    Gebaeude = pd.DataFrame.from_records(json.loads(Gebaeude_raw))
    Gebaeude = Gebaeude.set_index('Beschreibung')
    
    print("GWh_Jahr_Ah_Zelle_raw")
    print(GWh_Jahr_Ah_Zelle_raw["GWh_pro_jahr"])
    
    #____________________________________
    #Kostenrechnung
    
    #leeres DataFrame, wird später gefüllt
    df = pd.DataFrame()
    
    #Anfangsdictionary das dem letzten Schritt übergeben wird, zusätzlich stellt es den Index der Tabelle dar
    # Anfangsmengenwerte errechnen aus dem Zelläquivalent: "wie viel Anodenbeschichtung braucht man für eine Zelle
    
    # Anodenbeschichtung NOCH ÜBERARBEITEN
    Anodenbeschichtung_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/1000 #[kg]
    
    # Kathodenbeschichtung
    Kathodenbeschichtung_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/1000 #[kg]
    
    #Anodenkollektor
    Anodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0] #Raussuchen, welcher Anodenkollektor verwendet wurde
    print(Anodenkollektor)
    Anodenkollektor_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]

    #Kathodenkollektor
    Kathodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0] #Raussuchen, welcher Kathodenkollektor verwendet wurde
    Kathodenkollektor_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]
    
    # Separator NOCH ÜBERARBEITEN
    Separator = Zellchemie.loc[Zellchemie['Kategorie'] == "Separator"].index.tolist()[0] #Raussuchen, welcher Separator verwendet wurde
    Separator_menge = Kathodenkollektor_menge*2
    
    #Elektrolyt
    Elektrolyt = Zellchemie.loc[Zellchemie['Kategorie'] == "Elektrolyt"].index.tolist()[0] #Raussuchen, welches Elektrolyt verwendet wurde
    Elektrolyt_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Elektrolyt"]/read_materialinfo(Elektrolyt)["Wert"]["Dichte"]/1000 #[l]
    
    schritt_dictionary={
         "Zelläquivalent":Zellergebnisse["Wert"]["Zellen pro Jahr"],
         "Anodenbeschichtung":Anodenbeschichtung_menge,
         "Kathodenbeschichtung":Kathodenbeschichtung_menge,
         "Anodenkollektor": Anodenkollektor_menge,
         "Kathodenkollektor": Kathodenkollektor_menge,
         "Separator":Separator_menge,
         "Elektrolyt":Elektrolyt_menge,
         "Anzahl Maschinen":"",
         "Neue Materialien":"",
         "Flächenbedarf":"",
         "Flächenbedarf Trockenraum":"",
         "Flächenbedarf Labor":"",
         "Personlabedarf Facharbeiter":"",
         "Personalbedarf Hilfskraft":"",
         "Energiebedarf":"",
         'Materialkosten':"",
         'Personalkosten':"",
         'Energiekosten':"",
         'Instandhaltungskosten':"",
         'Flächenkosten':"",
         'Kalkulatorische Zinsen':"",
         'Ökonomische Abschreibung':"",
         'Investition':""
         
         }
    
    #Gleiches Dictionary wie zuvor, mit den entsprechenden Einheiten 
    schritt_dictionary_einheiten={
         "Zelläquivalent":"-",
         "Anodenbeschichtung":"kg",
         "Kathodenbeschichtung":"kg",
         "Anodenkollektor":"m",
         "Kathodenkollektor":"m",
         "Separator":"m",
         "Elektrolyt":"l",
         "Anzahl Maschinen":"-",
         "Neue Materialien":"-",
         "Flächenbedarf":"m²",
         "Flächenbedarf Trockenraum":"m²",
         "Flächenbedarf Labor":"m²",
         "Personlabedarf Facharbeiter":"-",
         "Personalbedarf Hilfskraft":"-",
         "Energiebedarf":"kWh",
         'Materialkosten': '€', 
         'Personalkosten': '€', 
         'Energiekosten': '€', 
         'Instandhaltungskosten': '€', 
         'Flächenkosten': '€', 
         'Kalkulatorische Zinsen': '€', 
         'Ökonomische Abschreibung': '€', 
         'Investition': '€'
         }
    
    #erste Spalte (index) in das df einfügen 
    df["index"] = schritt_dictionary.keys()
    
    #erste Spalte zum Index umformen
    df = df.set_index('index')
        
    #____________________________________
    #Materialrückgewinnung
    #Zelle: Das Material, welches am Ende in der Zelle landet
    #Gesamt: Das die Menge des Materials, die zum Prozess zugeeführt wird 
    rueckgewinnung_dict_temp = [{"Material":"Anodenbeschichtung","Zelle":Anodenbeschichtung_menge,"Gesamt":""},
                           {"Material":"Kathodenbeschichtung","Zelle":Kathodenbeschichtung_menge,"Gesamt":""},
                           {"Material":"Anodenkollektor","Zelle":Anodenkollektor_menge,"Gesamt":""},
                           {"Material":"Kathodenkollektor","Zelle":Kathodenkollektor_menge,"Gesamt":""},
                           {"Material":"Separator","Zelle":Separator_menge,"Gesamt":""},
                           {"Material":"Elektrolyt","Zelle":Elektrolyt_menge,"Gesamt":""},
                           ]
    rueckgewinnung_dict = []
    
    #____________________________________
    #Retrograde Materialflusskalkulation
    
    for schritt in reversed(Prozessroute_array_raw):        #Prozessschritte in umgekehrter Reihenfolge durchgehen
        Prozess_name = schritt                          #Kopie des Schritts zur Umwandlung in Funktionsname, ersetzen aller Sonderzeichen durch "_"
        Prozess_name = Prozess_name.replace(' ','_').replace('-','_').replace('/','_')    
        #Übergebene Parameter and die Funtionen zu jedem Schritt: read_prozessInfo(schritt):  , 
        schritt_dictionary = getattr(Prozessfunktionen, Prozess_name)(read_prozessInfo(schritt), #df mit den Infos zum Prozesschritt
                                                                      Zellergebnisse, #Zellergebnisse: Ergebnisse der Zellberechnung
                                                                      Zellchemie, #die Zellchemie
                                                                      Materialinfos, #Infos zu den Materialien
                                                                      schritt_dictionary #schritt_dictionary: die Parameter die zwischen den Schritten übergeben werden
                                                                      )  

        #die Informationen jedes Prozessschrittes in das df einfügen
        df[schritt] = df.index.to_series().map(schritt_dictionary)
    
    #____________________________________
    #Abschluss Retrograde Materialflusskalkulation
    
    
    #____________________________________
    #Berechnung der jährlichen Flächenkosten/m², der Investkosten für den Bau und der Flächen 

    flaeche_normalraum = sum(list(df.loc["Flächenbedarf"]))
    flaeche_trockenraum = sum(list(df.loc["Flächenbedarf Trockenraum"]))

    flaechenergebnisse = flaechenberechnung(flaeche_normalraum, flaeche_trockenraum, Gebaeude, Oekonomische_Parameter)
    grundstueckskosten = flaechenergebnisse[0]
    flaechenverteilung = flaechenergebnisse[1]
    flaechenkosten_jaehrlich = flaechenergebnisse[2]
    fabrikflaeche = flaechenergebnisse[3]
    Fabrikflaeche_ohne_Produktion = flaechenergebnisse[4]
    
    
    
    
    #____________________________________
    #Anterograde Wertstromkalkulation  
    #Bestimmen der Einzelkosten
    #Betriebstage = Mitarbeiter_und_Logistik["Wert"]["Betriebstage"]
    Betriebstage = 365
    
    Materialkosten = {
        "Anodenbeschichtung_kosten":Zellergebnisse["Wert"]["Kilopreis Anodenbeschichtung"], #[€/kg]
        "Kathodenbeschichtung_kosten":Zellergebnisse["Wert"]["Kilopreis Kathodenbeschichtung"], #[€/kg]
        "Anodenkollektor_kosten":read_materialinfo(Anodenkollektor)["Wert"]["Preis"], #[€/m²]
        "Kathodenkollektor_kosten":read_materialinfo(Kathodenkollektor)["Wert"]["Preis"], #[€/m²]
        "Separator_kosten":read_materialinfo(Separator)["Wert"]["Preis"], #[€/m²]
        "Elektrolyt_kosten":read_materialinfo(Elektrolyt)["Wert"]["Preis"] #[€/kg]
        }
    
    Strompreis = Oekonomische_Parameter["Wert"]["Energiekosten"] #[€/kWh]
    Stundensatz_hilfskraft = Mitarbeiter_und_Logistik["Wert"]["Stundensatz Hilfskraft"] #[€/h]
    Stundensatz_facharbeiter = Mitarbeiter_und_Logistik["Wert"]["Stundensatz Facharbeiter"] #[€/h]
    Instandhaltungskostensatz = Oekonomische_Parameter["Wert"]["Instandhaltungskostensatz"] #[%]
    Flächenkosten_Produktionshalle = flaechenkosten_jaehrlich #[€/m²] dauerhafte Kosten pro Jahr?
    Flächenkosten_Trockenraum = flaechenkosten_jaehrlich  #[€/m²] dauerhafte Kosten pro Jahr?
    Stromverbrauch_Trockenraum_Flächennormiert = Gebaeude["Wert"]["Energie Trockenraum flächennormiert"]  #[€/m²] dauerhafte Kosten pro Jahr?
    Zinssatz_Kapitalmarkt = Oekonomische_Parameter["Wert"]["Kapitalkosten"]/100 #[%]
    Nutzungsdauer = Oekonomische_Parameter["Wert"]["technische Nutzungsdauer"] #[%]
    
    Materialkosten_dict = {}
    for schritt in Prozessroute_array_raw:
        
        #Materialkosten
        if df[schritt]["Neue Materialien"]!="":
            liste = df[schritt]["Neue Materialien"].split(";")
            kosten = 0
            for material in liste:
                print(material)
                cost = df[schritt][material]*Materialkosten[material+"_kosten"] 
                print(cost)
                kosten += df[schritt][material]*Materialkosten[material+"_kosten"] 
                print(kosten)
                Materialkosten_dict.update({material:round(cost,2)})
                
                for rueck_material in rueckgewinnung_dict_temp:
                    if material == rueck_material["Material"]:
                        rueck_material["Gesamt"]=df[schritt][material]
                        rueckgewinnung_dict.append(rueck_material)
                        
            df[schritt]["Materialkosten"]=kosten
        else:
            df[schritt]["Materialkosten"]=0
            
        #Energiekosten
        df[schritt]["Energiekosten"] = df[schritt]["Energiebedarf"]*Strompreis+df[schritt]["Flächenbedarf Trockenraum"]*Stromverbrauch_Trockenraum_Flächennormiert*Betriebstage
        
        #Personalkosten
        df[schritt]["Personalkosten"] = (df[schritt]["Personlabedarf Facharbeiter"]*Stundensatz_facharbeiter + df[schritt]["Personalbedarf Hilfskraft"]*Stundensatz_hilfskraft)*Betriebstage*24

        #Instandhaltungskosten
        df[schritt]["Instandhaltungskosten"] = df[schritt]["Investition"]*(Instandhaltungskostensatz/100)
        
        #Flächenkosten
        df[schritt]["Flächenkosten"] = df[schritt]["Flächenbedarf"]*Flächenkosten_Produktionshalle+df[schritt]["Flächenbedarf Trockenraum"]*Flächenkosten_Trockenraum
    
        #Kalkulatorische Zinsen
        df[schritt]["Kalkulatorische Zinsen"]=df[schritt]["Investition"]*1.1*Zinssatz_Kapitalmarkt/100/0.5
        
        #Ökonomische Abschreibung
        df[schritt]["Ökonomische Abschreibung"]=df[schritt]["Investition"]/Nutzungsdauer
    #Abschluss Anterograde Wertstromkalkulation   
    
    
    #OVERHEAD KOSTEN
    #____________________________________
    #Flächenkalkulation    

    #Abschluss Flächenkalkulation

    
    Personalkosten_overhead = sum([sum(list(df.loc[x])) for x in ["Personlabedarf Facharbeiter","Personalbedarf Hilfskraft"]])*24*Betriebstage*(
        Mitarbeiter_und_Logistik["Wert"]["Stundensatz Indirekte"]*1/Mitarbeiter_und_Logistik["Wert"]["Führunggspanne"]+
        Mitarbeiter_und_Logistik["Wert"]["Stundensatz Reinigungskräfte"]*1/Mitarbeiter_und_Logistik["Wert"]["Spanne Reinigungskräfte"])

    Klimatisierung_overhead = fabrikflaeche*Gebaeude["Wert"]["Mediengrundversorgung"]*24*Betriebstage*Oekonomische_Parameter["Wert"]["Energiekosten"]/1000

    Flaechenkosten_overhead = Fabrikflaeche_ohne_Produktion*flaechenkosten_jaehrlich
        
    fix_cost = Personalkosten_overhead + Klimatisierung_overhead + sum(list(df.loc["Instandhaltungskosten"])) #Overhead Kosten

    overhead_kosten = [
        {
            "group": "Personalkosten",
            "value": Personalkosten_overhead
        },
        {
            "group": "Flächenkosten",
            "value": Flaechenkosten_overhead
        },
        {
            "group": "Klimatisierung",
            "value": Klimatisierung_overhead
        }
    ]
    
    
    
    #____________________________________
    #Overhead Personal
    
    #Abschluss Overhead Personal   
        
        
        
    #____________________________________
    #Klimatisierung
    
    #Abschluss Klimatisierung 
                
        
        
    #____________________________________
    #Steuer
    
    #Abschluss Steuer
                        
        
        
    #____________________________________
    #Investitions-Overhead
    
    #Abschluss Investitions-Overhead
                        
        
        
    #____________________________________
    #Entsorgung
    
    #Abschluss Entsorgung    
                        
        
        
    #____________________________________
    #ORamp up
    
    #Abschluss Ramp up    


    #____________________________________
    #Levelized costs

    levelized_cost_result = levelized_cost(
        construction_cost_factory = sum(anteil["value"] for anteil in grundstueckskosten),
        lifetime_factory = Gebaeude["Wert"]["Nutzungsdauer"],
        interest_rate = Oekonomische_Parameter["Wert"]["Kapitalkosten"]/100,
        tax_rate = Oekonomische_Parameter["Wert"]["Umsatzsteuer"]/100,
        variable_cost = sum([sum(list(df.loc[x])) for x in ["Materialkosten",
                                                        "Personalkosten",
                                                        "Energiekosten",
                                                        #"Instandhaltungskosten",
                                                        #"Flächenkosten",
                                                        #"Kalkulatorische Zinsen",
                                                        #"Ökonomische Abschreibung"
                                                        ]]),
        fix_cost = fix_cost,
        output_kWh = float(GWh_Jahr_Ah_Zelle_raw["GWh_pro_jahr"])*1000000,
        machine_invest = sum(list(df.loc["Investition"])),
        factory_depreciation = Oekonomische_Parameter["Wert"]["Abschreibungsdauer Gebäude"],
        machine_depreciation = Oekonomische_Parameter["Wert"]["technische Nutzungsdauer"]
    )
    
    
    #____________________________________
    #Umformen des df
    
    print(Materialkosten_dict)
    
    #Einheiten einfügen
    df["Einheit"] = df.index.to_series().map(schritt_dictionary_einheiten)
    #Index wieder als Spalte einfügen
    df['index'] = df.index.tolist()
    #Zeile "neue Materialien" entfernen, ist in der Anzeige irrelevant/ irreführend
    df = df.drop("Neue Materialien",axis=0)
    #Reihenfolge im df drehen
    df = df.iloc[:, ::-1] 
    
    return(df,Materialkosten_dict, rueckgewinnung_dict, grundstueckskosten, flaechenverteilung, levelized_cost_result, overhead_kosten)
#Kostenberechnung()