# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 18:06:34 2022

@author: bendzuck
"""
import pandas as pd
import json
import math
import copy
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
                     GWh_Jahr_Ah_Zelle_raw,
                     rueckgewinnung_raw):
   
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

    rueckgewinnung = pd.DataFrame.from_records(json.loads(rueckgewinnung_raw))
    rueckgewinnung = rueckgewinnung.set_index('Beschreibung')
    
    #____________________________________
    #Kostenrechnung
    
    #leeres DataFrame, wird sp??ter gef??llt
    df = pd.DataFrame()
    
    #Anfangsdictionary das dem letzten Schritt ??bergeben wird, zus??tzlich stellt es den Index der Tabelle dar
    # Anfangsmengenwerte errechnen aus dem Zell??quivalent: "wie viel Anodenbeschichtung braucht man f??r eine Zelle
    
    # Anodenbeschichtung NOCH ??BERARBEITEN
    Anodenbeschichtung_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/1000 #[kg]
    
    # Kathodenbeschichtung
    Kathodenbeschichtung_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/1000 #[kg]
    
    #Anodenkollektor
    Anodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0] #Raussuchen, welcher Anodenkollektor verwendet wurde
    Anodenkollektor_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]

    #Kathodenkollektor
    Kathodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0] #Raussuchen, welcher Kathodenkollektor verwendet wurde
    Kathodenkollektor_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]
    
    # Separator NOCH ??BERARBEITEN
    Separator = Zellchemie.loc[Zellchemie['Kategorie'] == "Separator"].index.tolist()[0] #Raussuchen, welcher Separator verwendet wurde
    Separator_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Fl??che Separator gesamt"]/1e6 #[m??]
    #Separator_menge = Anodenkollektor_menge*2
    
    #Elektrolyt
    Elektrolyt = Zellchemie.loc[Zellchemie['Kategorie'] == "Elektrolyt"].index.tolist()[0] #Raussuchen, welches Elektrolyt verwendet wurde
    Elektrolyt_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"]*Zellergebnisse["Wert"]["Gewicht Elektrolyt"]/read_materialinfo(Elektrolyt)["Wert"]["Dichte"]/1000 #[l]
    
    #H??lle
    Huelle = Zellchemie.loc[Zellchemie['Kategorie'] == "H??lle"].index.tolist()[0] #Raussuchen, welches Elektrolyt verwendet wurde
    Huelle_menge = Zellergebnisse["Wert"]["Zellen pro Jahr"] #[-]


    schritt_dictionary={
         "Zell??quivalent":Zellergebnisse["Wert"]["Zellen pro Jahr"],
         "Anodenbeschichtung":Anodenbeschichtung_menge,
         "Kathodenbeschichtung":Kathodenbeschichtung_menge,
         "Anodenkollektor": Anodenkollektor_menge,
         "Kathodenkollektor": Kathodenkollektor_menge,
         "Separator":Separator_menge,
         "H??lle":Huelle_menge,
         "Elektrolyt":Elektrolyt_menge,
         "Anodenbeschichtung R??ckgewinnung":0,
         "Kathodenbeschichtung R??ckgewinnung":0,
         "Anodenkollektor R??ckgewinnung": 0,
         "Kathodenkollektor R??ckgewinnung": 0,
         "Separator R??ckgewinnung":0,
         "H??lle R??ckgewinnung":0,
         "Elektrolyt R??ckgewinnung":0,
         "Anzahl Maschinen":"",
         "Neue Materialien":"",
         "Fl??chenbedarf":"",
         "Fl??chenbedarf Trockenraum":"",
         "Fl??chenbedarf Labor":"",
         "Personlabedarf Facharbeiter":"",
         "Personalbedarf Hilfskraft":"",
         "Energiebedarf":"",
         'Materialkosten':"",
         'Personalkosten':"",
         'Energiekosten':"",
         'Instandhaltungskosten':"",
         'Fl??chenkosten':"",
         'Kalkulatorische Zinsen':"",
         '??konomische Abschreibung':"",
         'Investition':""
         
         }
    
    #Gleiches Dictionary wie zuvor, mit den entsprechenden Einheiten 
    schritt_dictionary_einheiten={
         "Zell??quivalent":"-",
         "Anodenbeschichtung":"kg",
         "Kathodenbeschichtung":"kg",
         "Anodenkollektor":"m",
         "Kathodenkollektor":"m",
         "Separator":"m??",
         "H??lle":"-",
         "Elektrolyt":"l",
         "Anodenbeschichtung R??ckgewinnung":"kg",
         "Kathodenbeschichtung R??ckgewinnung":"kg",
         "Anodenkollektor R??ckgewinnung":"m",
         "Kathodenkollektor R??ckgewinnung":"m",
         "Separator R??ckgewinnung":"m??",
         "H??lle R??ckgewinnung":"m??",
         "Elektrolyt R??ckgewinnung":"l",
         "Anzahl Maschinen":"-",
         "Neue Materialien":"-",
         "Fl??chenbedarf":"m??",
         "Fl??chenbedarf Trockenraum":"m??",
         "Fl??chenbedarf Labor":"m??",
         "Personlabedarf Facharbeiter":"-",
         "Personalbedarf Hilfskraft":"-",
         "Energiebedarf":"kWh",
         'Materialkosten': '???', 
         'Personalkosten': '???', 
         'Energiekosten': '???', 
         'Instandhaltungskosten': '???', 
         'Fl??chenkosten': '???', 
         'Kalkulatorische Zinsen': '???', 
         '??konomische Abschreibung': '???', 
         'Investition': '???'
         }
    
    #erste Spalte (index) in das df einf??gen 
    df["index"] = schritt_dictionary.keys()
    
    #erste Spalte zum Index umformen
    df = df.set_index('index')
        
    #____________________________________
    #Materialr??ckgewinnung
    #Zelle: Das Material, welches am Ende in der Zelle landet
    #Gesamt: Das die Menge des Materials, die zum Prozess zugeef??hrt wird 
    rueckgewinnung_dict_temp = [{"Material":"Anodenbeschichtung","Zelle":Anodenbeschichtung_menge,"Gesamt":""},
                           {"Material":"Kathodenbeschichtung","Zelle":Kathodenbeschichtung_menge,"Gesamt":""},
                           {"Material":"Anodenkollektor","Zelle":Anodenkollektor_menge,"Gesamt":""},
                           {"Material":"Kathodenkollektor","Zelle":Kathodenkollektor_menge,"Gesamt":""},
                           {"Material":"Separator","Zelle":Separator_menge,"Gesamt":""},
                           {"Material":"Elektrolyt","Zelle":Elektrolyt_menge,"Gesamt":""},
                           {"Material":"H??lle","Zelle":Huelle_menge,"Gesamt":""},
                           ]
    rueckgewinnung_dict = []
    
    #____________________________________
    #Retrograde Materialflusskalkulation
    
    for schritt in reversed(Prozessroute_array_raw):        #Prozessschritte in umgekehrter Reihenfolge durchgehen
        Prozess_name = schritt                          #Kopie des Schritts zur Umwandlung in Funktionsname, ersetzen aller Sonderzeichen durch "_"
        Prozess_name = Prozess_name.replace(' ','_').replace('-','_').replace('/','_')    
        #??bergebene Parameter and die Funtionen zu jedem Schritt: read_prozessInfo(schritt):  , 
        schritt_dictionary = getattr(Prozessfunktionen, Prozess_name)(read_prozessInfo(schritt), #df mit den Infos zum Prozesschritt
                                                                      Zellergebnisse, #Zellergebnisse: Ergebnisse der Zellberechnung
                                                                      Zellchemie, #die Zellchemie
                                                                      Materialinfos, #Infos zu den Materialien
                                                                      schritt_dictionary, #schritt_dictionary: die Parameter die zwischen den Schritten ??bergeben werden
                                                                      rueckgewinnung #dictionary zu den Anteilen die zur??ck gewonnen werden k??nnen
                                                                      )  

        #die Informationen jedes Prozessschrittes in das df einf??gen
        df[schritt] = df.index.to_series().map(schritt_dictionary)
    
    #____________________________________
    #Abschluss Retrograde Materialflusskalkulation
    
    
    #____________________________________
    #Berechnung der j??hrlichen Fl??chenkosten/m??, der Investkosten f??r den Bau und der Fl??chen 

    flaeche_normalraum = sum(list(df.loc["Fl??chenbedarf"]))
    flaeche_trockenraum = sum(list(df.loc["Fl??chenbedarf Trockenraum"]))
    flaeche_labor = sum(list(df.loc["Fl??chenbedarf Labor"]))

    flaechenergebnisse = flaechenberechnung(flaeche_normalraum, flaeche_trockenraum, Gebaeude, Oekonomische_Parameter,flaeche_labor)
    grundstueckskosten = flaechenergebnisse[0]
    flaechenverteilung = flaechenergebnisse[1]
    flaechenkosten_jaehrlich = flaechenergebnisse[2]
    fabrikflaeche = flaechenergebnisse[3]
    Fabrikflaeche_ohne_Produktion = flaechenergebnisse[4]
    

    #____________________________________
    #Anterograde Wertstromkalkulation  
    #Bestimmen der Einzelkosten
    #Betriebstage = Mitarbeiter_und_Logistik["Wert"]["Betriebstage"]
    Betriebstage = 360
    
    Materialkosten = {
        "Anodenbeschichtung_kosten":Zellergebnisse["Wert"]["Kilopreis Anodenbeschichtung"], #[???/kg]
        "Kathodenbeschichtung_kosten":Zellergebnisse["Wert"]["Kilopreis Kathodenbeschichtung"], #[???/kg]
        #"Anodenkollektor_kosten":read_materialinfo(Anodenkollektor)["Wert"]["Preis"], #[???/m??]
        #"Kathodenkollektor_kosten":read_materialinfo(Kathodenkollektor)["Wert"]["Preis"], #[???/m??]
        "Anodenkollektor_kosten":read_materialinfo(Anodenkollektor)["Wert"]["Preis"]*read_materialinfo(Anodenkollektor)["Wert"]["Breite"]/1000, #[???/m]
        "Kathodenkollektor_kosten":read_materialinfo(Kathodenkollektor)["Wert"]["Preis"]*read_materialinfo(Kathodenkollektor)["Wert"]["Breite"]/1000, #[???/m]
        "Separator_kosten":read_materialinfo(Separator)["Wert"]["Preis"], #[???/m??]
        "Elektrolyt_kosten":read_materialinfo(Elektrolyt)["Wert"]["Preis"], #[???/kg]
        "H??lle_kosten":read_materialinfo(Huelle)["Wert"]["Preis"] #[???/m??]
        }
    
    Strompreis = Oekonomische_Parameter["Wert"]["Energiekosten"] #[???/kWh]
    Stundensatz_hilfskraft = Mitarbeiter_und_Logistik["Wert"]["Stundensatz Hilfskraft"] #[???/h]
    Stundensatz_facharbeiter = Mitarbeiter_und_Logistik["Wert"]["Stundensatz Facharbeiter"] #[???/h]
    Instandhaltungskostensatz = Oekonomische_Parameter["Wert"]["Instandhaltungskostensatz"] #[%]
    Fl??chenkosten_Produktionshalle = flaechenkosten_jaehrlich #[???/m??] dauerhafte Kosten pro Jahr?
    Fl??chenkosten_Trockenraum = flaechenkosten_jaehrlich  #[???/m??] dauerhafte Kosten pro Jahr?
    Stromverbrauch_Trockenraum_Fl??chennormiert = Gebaeude["Wert"]["Energie Trockenraum fl??chennormiert"]  #[???/m??] dauerhafte Kosten pro Jahr?
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
                print(df[schritt][material])

                cost = df[schritt][material]*Materialkosten[material+"_kosten"] 

                kosten += df[schritt][material]*Materialkosten[material+"_kosten"] 

                Materialkosten_dict.update({material:round(cost,2)})
                
                for rueck_material in rueckgewinnung_dict_temp:
                    if material == rueck_material["Material"]:
                        rueck_material["Gesamt"]=df[schritt][material]
                        rueckgewinnung_dict.append(rueck_material)
                        
            df[schritt]["Materialkosten"]=kosten
        else:
            df[schritt]["Materialkosten"]=0
            
        #Energiekosten
        df[schritt]["Energiekosten"] = df[schritt]["Energiebedarf"]*Strompreis+df[schritt]["Fl??chenbedarf Trockenraum"]*Stromverbrauch_Trockenraum_Fl??chennormiert*Betriebstage+df[schritt]["Fl??chenbedarf Labor"]*Betriebstage*Gebaeude["Wert"]["Energie Labor fl??chennormiert"]
        
        #Personalkosten
        df[schritt]["Personalkosten"] = (df[schritt]["Personlabedarf Facharbeiter"]*Stundensatz_facharbeiter + df[schritt]["Personalbedarf Hilfskraft"]*Stundensatz_hilfskraft)*Betriebstage*24

        #Instandhaltungskosten
        df[schritt]["Instandhaltungskosten"] = df[schritt]["Investition"]*(Instandhaltungskostensatz/100)
        
        #Fl??chenkosten
        df[schritt]["Fl??chenkosten"] = df[schritt]["Fl??chenbedarf"]*Fl??chenkosten_Produktionshalle+df[schritt]["Fl??chenbedarf Trockenraum"]*Fl??chenkosten_Trockenraum+df[schritt]["Fl??chenbedarf Labor"]*flaechenkosten_jaehrlich
    
        #Kalkulatorische Zinsen
        df[schritt]["Kalkulatorische Zinsen"]=df[schritt]["Investition"]*1.1*Zinssatz_Kapitalmarkt/100/0.5
        
        #??konomische Abschreibung
        df[schritt]["??konomische Abschreibung"]=df[schritt]["Investition"]/Nutzungsdauer
    #Abschluss Anterograde Wertstromkalkulation   
    
    
    #OVERHEAD KOSTEN
    #____________________________________
    #Fl??chenkalkulation    

    #Abschluss Fl??chenkalkulation

    
    Personalkosten_overhead = sum([sum(list(df.loc[x])) for x in ["Personlabedarf Facharbeiter","Personalbedarf Hilfskraft"]])*24*Betriebstage*(
        Mitarbeiter_und_Logistik["Wert"]["Stundensatz Indirekte"]*1/Mitarbeiter_und_Logistik["Wert"]["F??hrunggspanne"]+
        Mitarbeiter_und_Logistik["Wert"]["Stundensatz Reinigungskr??fte"]*1/Mitarbeiter_und_Logistik["Wert"]["Spanne Reinigungskr??fte"])

    Klimatisierung_overhead = fabrikflaeche*Gebaeude["Wert"]["Mediengrundversorgung"]*Oekonomische_Parameter["Wert"]["Energiekosten"]/1000

    Flaechenkosten_overhead = Fabrikflaeche_ohne_Produktion*flaechenkosten_jaehrlich
        
    fix_cost = Personalkosten_overhead + Klimatisierung_overhead + sum(list(df.loc["Instandhaltungskosten"])) #Overhead Kosten

    overhead_kosten = [
        {
            "group": "Personalkosten",
            "value": Personalkosten_overhead
        },
        {
            "group": "Fl??chenkosten",
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

    Materialkosten_mit_rueckgewinnung = {}
    for Material in Materialkosten_dict:
        Materialkosten_mit_rueckgewinnung[Material]=Materialkosten_dict[Material]-sum(list(df.loc[Material+" R??ckgewinnung"]))*Materialkosten[Material+"_kosten"]



    #____________________________________
    #Levelized costs

    levelized_cost_result = levelized_cost(
        construction_cost_factory = sum(anteil["value"] for anteil in grundstueckskosten),
        lifetime_factory = Gebaeude["Wert"]["Nutzungsdauer"],
        interest_rate = Oekonomische_Parameter["Wert"]["Kapitalkosten"]/100,
        tax_rate = Oekonomische_Parameter["Wert"]["Umsatzsteuer"]/100,
        #variable_cost = sum([sum(list(df.loc[x])) for x in ["Materialkosten",
        #                                                "Personalkosten",
        #                                                "Energiekosten",
                                                        #"Instandhaltungskosten",
                                                        #"Fl??chenkosten",
                                                        #"Kalkulatorische Zinsen",
                                                        #"??konomische Abschreibung"
        #                                                ]]),
        Materialkosten = sum(list(df.loc["Materialkosten"])),
        Materialkosten_mit_rueckgewinnung = sum(Materialkosten_mit_rueckgewinnung.values()),
        Personalkosten = sum(list(df.loc["Personalkosten"])),
        Energiekosten = sum(list(df.loc["Energiekosten"])),
        fix_cost = fix_cost,
        output_kWh = float(GWh_Jahr_Ah_Zelle_raw["GWh_pro_jahr"])*1000000,
        machine_invest = sum(list(df.loc["Investition"])),
        factory_depreciation = Oekonomische_Parameter["Wert"]["Abschreibungsdauer Geb??ude"],
        machine_depreciation = Oekonomische_Parameter["Wert"]["technische Nutzungsdauer"],
        ramp_up_material = Oekonomische_Parameter["Wert"]["Ramp-up cost Material"],
        ramp_up_personal_overhead = Oekonomische_Parameter["Wert"]["Ramp-up cost Mitarbeiter und Overhead"]
    )

    
    levelized_cost_aufgeteilt = levelized_cost_result[1]
    levelized_cost_result = levelized_cost_result[0]

    
    
    
    #____________________________________
    #Umformen des df

  
    
    #Einheiten einf??gen
    df["Einheit"] = df.index.to_series().map(schritt_dictionary_einheiten)
    #Index wieder als Spalte einf??gen
    df['index'] = df.index.tolist()
    #Zeile "neue Materialien" entfernen, ist in der Anzeige irrelevant/ irref??hrend
    df = df.drop("Neue Materialien",axis=0)
    #Reihenfolge im df drehen
    df = df.iloc[:, ::-1] 


    levelized_cost_aufgeteilt_rueckgewinnung = copy.deepcopy(levelized_cost_aufgeteilt)
    levelized_cost_aufgeteilt_rueckgewinnung[0]["value"] = sum(Materialkosten_mit_rueckgewinnung.values())

    return(df,Materialkosten_dict, rueckgewinnung_dict, grundstueckskosten, flaechenverteilung, levelized_cost_result, overhead_kosten,Materialkosten_mit_rueckgewinnung,levelized_cost_aufgeteilt,levelized_cost_aufgeteilt_rueckgewinnung)
#Kostenberechnung()