# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 12:12:40 2022

@author: bendzuck
"""
import pandas as pd
import json
import math


#____________________________________
# die Eingangsparameter
# 1. Zellchemie [df]
# 2. Materialinfos [df]
# 3. Zellmaße [df]
# 4. Name Zellformat &  Zelltyp [JSON Object -> String]
# 5. Gesamtladung einer Zelle [float] (nur Pouchzelle) -> muss aus dem Frontend in eigenen redux state
# 6. Größe Gigafabrik in GWh/Jahr [float] -> muss aus dem Frontend in eigenen redux state, kann sich mit Gesamtladung teilen
# -> Hülle fehlt noch gesamt    

#Zellchemie = '[{"id":1,"Beschreibung":"NCM 622","Kategorie":"Aktivmaterial Kathode","Wert":97.0,"Einheit":"%"},{"id":2,"Beschreibung":"Graphit","Kategorie":"Aktivmaterial Anode","Wert":96.5,"Einheit":"%"},{"id":3,"Beschreibung":"Kupferfolie 10 \u00b5m","Kategorie":"Kollektorfolie Anode","Wert":null,"Einheit":"%"},{"id":4,"Beschreibung":"Aluminiumfolie 8 \u00b5m","Kategorie":"Kollektorfolie Kathode","Wert":null,"Einheit":"%"},{"id":6,"Beschreibung":"Wasser","Kategorie":"L\u00f6semittel Anode","Wert":3.0,"Einheit":"%"},{"id":10,"Beschreibung":"Zellspannung","Kategorie":"Allgemeine Parameter","Wert":3.7,"Einheit":"V"},{"id":11,"Beschreibung":"Irreversibler Formierungsverlust","Kategorie":"Allgemeine Parameter","Wert":10.0,"Einheit":"%"},{"id":12,"Beschreibung":"Zieldichte Beschichtung Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":3.0,"Einheit":"g\/cm\u00b3"},{"id":13,"Beschreibung":"Beschichtungsporosit\u00e4t Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":25.0,"Einheit":"%"},{"id":14,"Beschreibung":"Fl\u00e4chenspezifische Kapazit\u00e4t Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":4.0,"Einheit":"mAh\/cm\u00b2"},{"id":15,"Beschreibung":"Feststoffgehalt Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":60.0,"Einheit":"%"},{"id":16,"Beschreibung":"Zieldichte Beschichtung Anode","Kategorie":"Elektrodenparameter Anode","Wert":1.6,"Einheit":"g\/cm\u00b3"},{"id":17,"Beschreibung":"Beschichtungsporosit\u00e4t Anode","Kategorie":"Elektrodenparameter Anode","Wert":34.0,"Einheit":"%"},{"id":18,"Beschreibung":"Fl\u00e4chenspezifische Kapazit\u00e4t Anode","Kategorie":"Elektrodenparameter Anode","Wert":3.2,"Einheit":"mAh\/cm\u00b2"},{"id":19,"Beschreibung":"Feststoffgehalt Anode","Kategorie":"Elektrodenparameter Anode","Wert":60.0,"Einheit":"%"},{"id":20,"Beschreibung":"Kalkulierter Anoden\u00fcberschuss","Kategorie":"Elektrodenparameter Anode","Wert":10.0,"Einheit":"%"},{"id":21,"Beschreibung":"NMP","Kategorie":"L\u00f6semittel Kathode","Wert":63.4,"Einheit":"%"},{"id":22,"Beschreibung":"ProZell Separator","Kategorie":"Separator","Wert":null,"Einheit":"%"},{"id":23,"Beschreibung":"K-Leitru\u00df 1","Kategorie":"Additive Kathode","Wert":3.0,"Einheit":"%"},{"id":24,"Beschreibung":"K-Leitru\u00df 2","Kategorie":"Additive Kathode","Wert":0.0,"Einheit":"%"},{"id":25,"Beschreibung":"K-Additiv","Kategorie":"Additive Kathode","Wert":1.0,"Einheit":"%"},{"id":26,"Beschreibung":"K-Binder 1","Kategorie":"Additive Kathode","Wert":3.0,"Einheit":"%"},{"id":27,"Beschreibung":"K-Binder 2","Kategorie":"Additive Kathode","Wert":0.0,"Einheit":"%"},{"id":28,"Beschreibung":"A-Leitru\u00df 1","Kategorie":"Additive Anode","Wert":1.0,"Einheit":"%"},{"id":29,"Beschreibung":"A-Leitru\u00df 2","Kategorie":"Additive Anode","Wert":0.0,"Einheit":"%"},{"id":31,"Beschreibung":"A-Binder 1","Kategorie":"Additive Anode","Wert":1.0,"Einheit":"%"},{"id":32,"Beschreibung":"A-Binder 2","Kategorie":"Additive Anode","Wert":1.5,"Einheit":"%"},{"id":33,"Beschreibung":"1M LiPF6 (EC: EMC 3:7 wt%) + 2 wt% VC","Kategorie":"Elektrolyt","Wert":null,"Einheit":"%"}]'
#Materialinfos = '[{"NCM 622":[{"id":3,"Beschreibung":"spezifische Kapazität","Wert":160,"Einheit":"mAh/g"},{"id":4,"Beschreibung":"Dichte","Wert":0.476,"Einheit":"g/cm³"},{"id":5,"Beschreibung":"Preis","Wert":25.75,"Einheit":"€/kg"}]},{"Graphit":[{"id":1,"Beschreibung":"spezifische Kapazität","Wert":330,"Einheit":"mAh/g"},{"id":2,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Preis","Wert":7.46,"Einheit":"€/kg"}]},{"Kupferfolie 10 µm":[{"id":1,"Beschreibung":"Dicke","Wert":10,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":8.96,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Breite","Wert":600,"Einheit":"mm"},{"id":4,"Beschreibung":"Preis","Wert":0.44,"Einheit":"€/m"}]},{"Aluminiumfolie 8 µm":[{"id":1,"Beschreibung":"Dicke","Wert":8,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":2.7,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Breite","Wert":600,"Einheit":"mm"},{"id":4,"Beschreibung":"Preis","Wert":0.2,"Einheit":"€/m"}]},{"Wasser":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":0.01,"Einheit":"€/kg"}]},{"NMP":[{"id":1,"Beschreibung":"Dichte","Wert":1.2,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":2.39,"Einheit":"€/kg"}]},{"ProZell Separator":[{"id":1,"Beschreibung":"Dicke","Wert":20,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":10,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Porosität","Wert":40,"Einheit":"%"},{"id":4,"Beschreibung":"Breite","Wert":600,"Einheit":"mm"},{"id":5,"Beschreibung":"Preis","Wert":0.5,"Einheit":"€/m"}]},{"K-Leitruß 1":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"K-Leitruß 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"K-Additiv":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":10,"Einheit":"€/kg"}]},{"K-Binder 1":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":18,"Einheit":"€/kg"}]},{"K-Binder 2":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":18,"Einheit":"€/kg"}]},{"A-Leitruß 1":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"A-Leitruß 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"A-Binder 1":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":1.5,"Einheit":"€/kg"}]},{"A-Binder 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":1.5,"Einheit":"€/kg"}]},{"1M LiPF6 (EC: EMC 3:7 wt%) + 2 wt% VC":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":7.44,"Einheit":"€/kg"}]}]'
#Zellformat = '[{"id":1,"Beschreibung":"Breite Anode","Wert":null,"Einheit":"mm"},{"id":2,"Beschreibung":"L\u00e4nge Anode","Wert":null,"Einheit":"mm"},{"id":3,"Beschreibung":"Breite Zellf\u00e4hnchen Anode","Wert":22.0,"Einheit":"mm"},{"id":4,"Beschreibung":"L\u00e4nge Zellf\u00e4hnchen Anode","Wert":30.0,"Einheit":"mm"},{"id":5,"Beschreibung":"Breite Kathode","Wert":null,"Einheit":"mm"},{"id":6,"Beschreibung":"L\u00e4nge Kathode","Wert":null,"Einheit":"mm"},{"id":7,"Beschreibung":"Breite Zellf\u00e4hnchen Kathode","Wert":22.0,"Einheit":"mm"},{"id":8,"Beschreibung":"L\u00e4nge Zellf\u00e4hnchen Kathode","Wert":32.5,"Einheit":"mm"},{"id":9,"Beschreibung":"Eckenradius","Wert":5.0,"Einheit":"mm"},{"id":10,"Beschreibung":"Breite Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":11,"Beschreibung":"L\u00e4nge Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":12,"Beschreibung":"H\u00f6he Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":13,"Beschreibung":"Radius Rundzelle","Wert":10.5,"Einheit":"mm"},{"id":14,"Beschreibung":"H\u00f6he Rundzelle","Wert":70.0,"Einheit":"mm"},{"id":15,"Beschreibung":"Radius Wickelkern","Wert":3.0,"Einheit":"mm"},{"id":16,"Beschreibung":"Zusatzwicklungen Separator","Wert":3.0,"Einheit":"[-]"},{"id":17,"Beschreibung":"Abstand Separator - H\u00fclle","Wert":2.0,"Einheit":"mm"},{"id":18,"Beschreibung":"\u00dcberstand Separator - Anode","Wert":2.0,"Einheit":"mm"},{"id":19,"Beschreibung":"\u00dcberstand Anode - Kathode","Wert":2.0,"Einheit":"mm"},{"id":20,"Beschreibung":"Unterdruck Zelle","Wert":2.0,"Einheit":"mbar"},{"id":21,"Beschreibung":"Elektrolytbef\u00fcllung","Wert":80.0,"Einheit":"%"},{"id":22,"Beschreibung":"Sicherheitsabstand Schneiden","Wert":20.0,"Einheit":"mm"},{"id":23,"Beschreibung":"Beschichtungsabstand Kathode","Wert":20.0,"Einheit":"mm"},{"id":24,"Beschreibung":"Beschichtungsabstand Anode","Wert":20.0,"Einheit":"mm"},{"id":25,"Beschreibung":"Breite Kathodenkollektor","Wert":300.0,"Einheit":"mm"},{"id":26,"Beschreibung":"Breite Anodenkollektor","Wert":300.0,"Einheit":"mm"}]'
#Weitere_Zellinfos = '{"id":13,"Beschreibung":"21700","Zellformat":"Rundzelle","Dateiname":"Zelle_21700"}'

def zellberechnung(Zellchemie_raw, Materialinfos_raw, Zellformat_raw, weitere_Zellinfos_raw, GWh_Jahr_Ah_Zelle_raw):
    #____________________________________
    # allgemeine Funktionen
    # Filtert aus der gesammelten Materialinfo Tabelle ein Material heraus und gibt es als df zurück 
    def read_zellinfo(Material):
        df = Materialinfos.loc[Materialinfos["Material"] == Material]
        return df
    
    # flaeche_mit_zellf errechnet die Fäche eines Sheets mit Zellfähnchen, inklusive der Radien
    def flaeche_mit_zellf(breite, laenge, breite_zellf, laenge_zellf, radius):
        return breite*laenge+breite_zellf*laenge_zellf-(4*radius**2-math.pi*radius**2)
    def flaeche_ohne_zellf(breite, laenge, radius):
        return breite*laenge-(3*radius**2-math.pi*radius**2)
    
    
    #_________________________________ 
    # Umformen der Rohdaten in DataFrames
    a_json = json.loads(Zellchemie_raw)
    Zellchemie = pd.DataFrame.from_records(a_json)
    Zellchemie = Zellchemie.set_index('Beschreibung')
    
    
    b_json = json.loads(Materialinfos_raw)
    complete_df = []
    for Material_tabelle in b_json:
        Material = list(Material_tabelle.keys())[0]
        for Spalte in Material_tabelle[Material]:
            Spalte["Material"]=Material
            complete_df.append(Spalte)
    Materialinfos = pd.DataFrame.from_records(complete_df)
    Materialinfos = Materialinfos.set_index('Beschreibung')
    
    
    d_json = json.loads(Zellformat_raw)
    Zellformat = pd.DataFrame.from_records(d_json)
    Zellformat = Zellformat.set_index('Beschreibung')
    
    
    e_json = json.loads(weitere_Zellinfos_raw)
    weitere_Zellinfos = pd.DataFrame.from_dict(e_json, orient="index")
    Zellname = weitere_Zellinfos[0]["Beschreibung"]
    Zelltyp = weitere_Zellinfos[0]["Zellformat"]
    
    GWh_Jahr_Ah_Zelle = json.loads(GWh_Jahr_Ah_Zelle_raw)
    
    #____________________________________
    #Werte auslesen
    # Materialien auslesen
    Aktivmaterial_Kathode = Zellchemie.loc[Zellchemie['Kategorie'] == "Aktivmaterial Kathode"].index[0] #String
    Kollektorfolie_Kathode = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index[0] #String
    Additive_Kathode = Zellchemie.loc[Zellchemie['Kategorie'] == "Additive Kathode"].index.to_list() #Liste
    Lösemittel_Kathode = Zellchemie.loc[Zellchemie['Kategorie'] == "Lösemittel Kathode"].index.to_list() #Liste
    
    Aktivmaterial_Anode = Zellchemie.loc[Zellchemie['Kategorie'] == "Aktivmaterial Anode"].index[0] #String
    Kollektorfolie_Anode = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index[0] #String
    Additive_Anode = Zellchemie.loc[Zellchemie['Kategorie'] == "Additive Anode"].index.to_list() #Liste
    Lösemittel_Anode = Zellchemie.loc[Zellchemie['Kategorie'] == "Lösemittel Anode"].index.to_list() #Liste
    
    Separator = Zellchemie.loc[Zellchemie['Kategorie'] == "Separator"].index[0] #String
    Huelle = Zellchemie.loc[Zellchemie['Kategorie'] == "Hülle"].index[0] #String
    
    Elektrolyt = Zellchemie.loc[Zellchemie['Kategorie'] == "Elektrolyt"].index[0] #String
    
    #Hülle = Zellchemie.loc[Zellchemie['Kategorie'] == "Hülle"].index[0] #String
    
    #____________________________________
    #Zellchemie Parameter auslegen, gelten für alle Zellparameter
    
    U = Zellchemie["Wert"]["Zellspannung"] #Zellspannung in Volt [V]
    delta_irr = Zellchemie["Wert"]["Irreversibler Formierungsverlust"] #Irreversibler Formierungsverlust in Prozent [%]
    C_flsp = Zellchemie["Wert"]["Flächenspezifische Kapazität Elektrode"] #[mAh/cm²]
    
    d_KK = Materialinfos.loc[Materialinfos["Material"] == Kollektorfolie_Kathode]["Wert"]["Dicke"] #[µm]
    roh_KK = Materialinfos.loc[Materialinfos["Material"] == Kollektorfolie_Kathode]["Wert"]["Dichte"] #[g/cm³]
    #C_flsp_K = Zellchemie["Wert"]["Flächenspezifische Kapazität Kathode"] #[mAh/cm²]
    C_sp_K = Materialinfos.loc[Materialinfos["Material"] == Aktivmaterial_Kathode]["Wert"]["spezifische Kapazität"] #[mAh/g]
    phi_KB = Zellchemie["Wert"]["Beschichtungsporosität Kathode"] #[%]
    x_PM_K = 100-Zellchemie["Wert"][Aktivmaterial_Kathode] #Masseanteil passiver Komponenten Kathode in Prozent [%]
    
    
    d_AK = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Dicke"] #[µm]   
    roh_AK = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Dichte"] #[g/cm³]
    #C_flsp_A = Zellchemie["Wert"]["Flächenspezifische Kapazität Anode"] #[mAh/cm²]
    C_sp_A = read_zellinfo(Aktivmaterial_Anode)["Wert"]["spezifische Kapazität"] #[mAh/g]
    phi_AB = Zellchemie["Wert"]["Beschichtungsporosität Anode"] #[%]
    x_PM_A = 100-Zellchemie["Wert"][Aktivmaterial_Anode] #Masseanteil passiver Komponenten Anode in Prozent [%]
    delta_A = Zellchemie["Wert"]["Kalkulierter Anodenüberschuss"] #[%]
    #delta_A = 10 #[%] kalkulierter Anodenüberschuss
     
    d_Sep = read_zellinfo(Separator)["Wert"]["Dicke"] #[µm]
    roh_sep = read_zellinfo(Separator)["Wert"]["Dichte"] #[g/cm³]
    phi_sep = read_zellinfo(Separator)["Wert"]["Porosität"] #[%]
    
    roh_elyt = read_zellinfo(Elektrolyt)["Wert"]["Dichte"] #[g/cm³]

    Wandstaerke = read_zellinfo(Huelle)["Wert"]["Dicke"] #[mm]
    
    
    #____________________________________
    #Zusammensetzung der Suspension auslesen, Kosten/ Dichte berechnen
    
    
    Bestandteile_Anodenbeschichtung = Additive_Anode #ohne Lösemittel
    Bestandteile_Anodenbeschichtung.append(Aktivmaterial_Anode) #ohne Lösemittel
    #Gesamtdichte_Anodenfeststoffe = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Anodenbeschichtung)
    Gesamtdichte_Anodenfeststoffe = 1/sum(Zellchemie["Wert"][x]/100/read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Anodenbeschichtung)
    Gesamtdichte_Anodenlösemittel = 1/sum(Zellchemie["Wert"][x]/100/read_zellinfo(x)["Wert"]["Dichte"] for x in Lösemittel_Anode)
    Gesamtdichte_Anodenbeschichtung = 1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100/Gesamtdichte_Anodenfeststoffe + (1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100)/Gesamtdichte_Anodenlösemittel)
    
    Kosten_Anodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Preis"] for x in Bestandteile_Anodenbeschichtung) #€/kg
    Kosten_Anodenkollektor = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Preis"] #[€/m]
        
    Bestandteile_Kathodenbeschichtung=Additive_Kathode #ohne Lösemittel
    Bestandteile_Kathodenbeschichtung.append(Aktivmaterial_Kathode) 
    #Gesamtdichte_Kathodenfeststoffe = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Kathodenbeschichtung)
    Gesamtdichte_Kathodenfeststoffe = 1/sum(Zellchemie["Wert"][x]/100/read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Kathodenbeschichtung)
    Gesamtdichte_Kathodenlösemittel = 1/sum(Zellchemie["Wert"][x]/100/read_zellinfo(x)["Wert"]["Dichte"] for x in Lösemittel_Kathode)
    Gesamtdichte_Kathodenbeschichtung = 1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100/Gesamtdichte_Kathodenfeststoffe + (1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100)/Gesamtdichte_Kathodenlösemittel)
    
    Kosten_Kathodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Preis"] for x in Bestandteile_Kathodenbeschichtung) #€/kg
    Kosten_Kathodenkollektor = read_zellinfo(Kollektorfolie_Kathode)["Wert"]["Preis"] #[€/m]
                
    Kosten_Separator = read_zellinfo(Separator)["Wert"]["Preis"] #[€/m]
    Kosten_Elektrolyt = read_zellinfo(Elektrolyt)["Wert"]["Preis"] #[€/kg]
            
    #GWh_pro_jahr = float(massemodell_eingaben["GWH_pro_jahr"]) #[-]
    GWh_pro_jahr = GWh_Jahr_Ah_Zelle["GWh_pro_jahr"] #[-]
    
    roh_KB = Gesamtdichte_Kathodenbeschichtung*(1-phi_KB/100) #[g/cm³]
    roh_AB = Gesamtdichte_Anodenbeschichtung*(1-phi_AB/100) #[g/cm³]

    
    #____________________________________
    # Elektrochemische Charakterisierung, gleich für alle Zelltypen
    
    MB_K = C_flsp/(1-delta_irr/100)/(C_sp_K*(1-x_PM_K/100)) #Massenbelegung Kathode [g/cm²]
    MB_A = C_flsp*(1+delta_A/100)/(C_sp_A*(1-x_PM_A/100)) #Massenbelegung Anode [g/cm²]
    
    d_KB = (MB_K/roh_KB)*10000 #Dicke Kathodenbeschichtung [µm]
    d_AB = (MB_A/roh_AB)*10000 #Dicke Anodenbeschichtung [µm]
    d_WHE = d_AK + 2*d_AB + d_KK + 2*d_KB + 2*d_Sep #Dicke einer Wiederholeinheit [µm]
    d_MWHE = d_AK + 2*d_AB + 2*d_Sep #Dicke modifizierte Wiederholeinheit [µm]
    
    
    #____________________________________
    #Zellmaße die für alle Zellen gelten
    
    elektrolytbefuellung = Zellformat["Wert"]["Elektrolytbefüllung"] #[%]

    Breite_Kathodenkollektor = read_zellinfo(Kollektorfolie_Kathode)["Wert"]["Breite"] #[mm]
    Breite_Anodenkollektor = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Breite"] #[mm]
    Breite_Separator = read_zellinfo(Separator)["Wert"]["Breite"] #[mm]
    
    #HARDCODED WERTE, BITTE ÄNDERN!
    #leeeeeres Bla Bla (bisher nur ausgelegt für Pouchzelle, nur dafür da das die Berechnung bei den anderen weiterhin funktioniert)
    
    #____________________________________
    # Ab hier die Berechnung der einzelnen Zelltypen
    if Zelltyp == "Pouchzelle gestapelt":
        eckenradius_elektrode = Zellformat["Wert"]["Eckenradius"] #[mm]

        Ah_pro_zelle = GWh_Jahr_Ah_Zelle["Ah_pro_Zelle"] #[Ah]
        #Maße der Zellfähnchen
        breite_anode_zellf = Zellformat["Wert"]["Breite Zellfähnchen Anode"] #[mm]
        breite_kathode_zellf = Zellformat["Wert"]["Breite Zellfähnchen Kathode"] #[mm]
        laenge_anode_zellf = Zellformat["Wert"]["Länge Zellfähnchen Anode"] #[mm]
        laenge_kathode_zellf = Zellformat["Wert"]["Länge Zellfähnchen Kathode"] #[mm]
        
        #Maße der Sheets
        breite_anode = Zellformat["Wert"]["Breite Anode"] #[mm]
        breite_kathode = Zellformat["Wert"]["Breite Kathode"] #[mm]
        laenge_anode = Zellformat["Wert"]["Länge Anode"] #[mm]
        laenge_kathode = Zellformat["Wert"]["Länge Kathode"] #[mm]
        
        #Abstände beim Schneiden der Sheets
        Schneid_abs_aus_A = Zellformat["Wert"]["Sicherheitsabstand Schneiden Anode"] #[mm] Abstand nach außen und zwischen den beschichteten Bahnen
        Schneid_abs_aus_K = Zellformat["Wert"]["Sicherheitsabstand Schneiden Kathode"] #[mm] Abstand nach außen und zwischen den beschichteten Bahnen
        Schneid_abs_bahnr_A = Zellformat["Wert"]["Beschichtungsabstand Anode in Bahnrichtung"] #[mm] Abstand zwischen den Sheets in Bahnrichtung
        Schneid_abs_bahnr_K = Zellformat["Wert"]["Beschichtungsabstand Kathode in Bahnrichtung"] #[mm] Abstand zwischen den Sheets in Bahnrichtung
        Schneid_abd_gg_bahnr_A = Zellformat["Wert"]["Beschichtungsabstand Anode quer zur Bahn"] #[mm] Abstand zwischen den Sheets gegen Bahnrichtung
        Schneid_abd_gg_bahnr_K = Zellformat["Wert"]["Beschichtungsabstand Kathode quer zur Bahn"] #[mm] Abstand zwischen den Sheets gegen Bahnrichtung
        
        #Überstand Separator über die Anode, für die Flächenberechnung des Separators
        ueberstand_separator_anode = Zellformat["Wert"]["Überstand Separator - Anode"] #[mm]
    
        #Flächen der Bestandteile (Sheets)
        A_KK = flaeche_mit_zellf(breite_kathode,laenge_kathode,breite_kathode_zellf,laenge_kathode_zellf,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_KB = flaeche_ohne_zellf(breite_kathode,laenge_kathode,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_AK = flaeche_mit_zellf(breite_anode,laenge_anode,breite_anode_zellf,laenge_anode_zellf,eckenradius_elektrode) #Fläche Anode [mm²]
        A_AB = flaeche_ohne_zellf(breite_anode,laenge_anode,eckenradius_elektrode) #Fläche Anode [mm²]
        A_Sep = flaeche_mit_zellf(breite_anode+2*ueberstand_separator_anode,laenge_anode+2*ueberstand_separator_anode,0,0, 0) #Fläche Separator [mm²]
    


        l_WHE = C_flsp*A_KB*2/100 #[mAh] Ladung einer Wiederholeinheit (doppelt beschichtete Kathode -> *2)
    
        #Anzahl der Wiederholeinheiten um auf die gesetzte Ah zu kommen, nach oben aufgerundet
        anzahl_WHE = math.ceil(Ah_pro_zelle*1000/l_WHE)
        
        A_AB_ges = A_AB*(anzahl_WHE+1)*2
        A_KB_ges = A_KB*anzahl_WHE*2
        A_AK_ges = A_AK*(anzahl_WHE+1)*2
        A_KK_ges = A_KK*anzahl_WHE*2.
        A_Sep_ges = A_Sep*(anzahl_WHE+1)*2

        #Außenmaße Zelle
        breite = breite_anode+ueberstand_separator_anode*2
        laenge = laenge_anode+ueberstand_separator_anode*2+laenge_anode_zellf
        faktor_gastasche = 1.5 #zusätzliche Pouchfolienfläche für Gastasche

        A_Huelle = 2*breite*laenge*faktor_gastasche

        #Meter Elektrode/Sheet
        #Anzahl Sheets übereinander (beschichtete Bahnen), normal (für Ausnutzungsgrad) und abgerundet & Sheets pro meter Elektrode (S_MA & S_MK)
        #Anode
        bahnen_bes_A_ausn = (Breite_Anodenkollektor-Schneid_abs_aus_A)/(2*(laenge_anode+laenge_anode_zellf)+Schneid_abs_aus_A+Schneid_abd_gg_bahnr_A)
        bahnen_bes_A = math.floor(bahnen_bes_A_ausn)
        bahnen_bes_A_ausn = round(bahnen_bes_A/bahnen_bes_A_ausn,4)*100
        S_MA = 1000/(breite_anode+Schneid_abs_bahnr_A)*bahnen_bes_A*2
        #Kathode
        bahnen_bes_K_ausn = (Breite_Kathodenkollektor-Schneid_abs_aus_K)/(2*(laenge_kathode+laenge_kathode_zellf)+Schneid_abs_aus_K+Schneid_abd_gg_bahnr_K)
        bahnen_bes_K = math.floor(bahnen_bes_K_ausn)
        bahnen_bes_K_ausn = round(bahnen_bes_K/bahnen_bes_K_ausn,4)*100
        S_MK = 1000/(breite_kathode+Schneid_abs_bahnr_K)*bahnen_bes_K*2          
        
        #nutzbarere Innenraum der Zelle, Fläche des Separators * Höhe des desammten Stacks + die modifizierte WHE
        vol_nutz_zelle = A_Sep * (math.ceil(anzahl_WHE) * d_WHE/1000 + d_MWHE/1000) #[mm³]
     
    
    if Zelltyp == "Hardcase gestapelt":
        Wandstärke = Wandstaerke #[mm]
        eckenradius_elektrode = Zellformat["Wert"]["Eckenradius"] #[mm]
        #Maße der Zellfähnchen
        breite_anode_zellf = Zellformat["Wert"]["Breite Zellfähnchen Anode"] #[mm]
        breite_kathode_zellf = Zellformat["Wert"]["Breite Zellfähnchen Kathode"] #[mm]
        laenge_anode_zellf = Zellformat["Wert"]["Länge Zellfähnchen Anode"] #[mm]
        laenge_kathode_zellf = Zellformat["Wert"]["Länge Zellfähnchen Kathode"] #[mm]

        #Außenmaße der Zelle
        breite_festhuelle = Zellformat["Wert"]["Breite Festhülle"]-2*Wandstärke #[mm]
        laenge_festhuelle = Zellformat["Wert"]["Länge Festhülle"]-2*Wandstärke #[mm]
        hoehe_festhuelle = Zellformat["Wert"]["Höhe Festhülle"]-2*Wandstärke #[mm]

        A_Huelle = 2*breite_festhuelle*laenge_festhuelle+2*breite_festhuelle*hoehe_festhuelle+2*laenge_festhuelle*hoehe_festhuelle
        
        #Abstände beim Schneiden der Sheets
        Schneid_abs_aus_A = Zellformat["Wert"]["Sicherheitsabstand Schneiden Anode"] #[mm] Abstand nach außen und zwischen den beschichteten Bahnen
        Schneid_abs_aus_K = Zellformat["Wert"]["Sicherheitsabstand Schneiden Kathode"] #[mm] Abstand nach außen und zwischen den beschichteten Bahnen
        Schneid_abs_bahnr_A = Zellformat["Wert"]["Beschichtungsabstand Anode in Bahnrichtung"] #[mm] Abstand zwischen den Sheets in Bahnrichtung
        Schneid_abs_bahnr_K = Zellformat["Wert"]["Beschichtungsabstand Kathode in Bahnrichtung"] #[mm] Abstand zwischen den Sheets in Bahnrichtung
        Schneid_abd_gg_bahnr_A = Zellformat["Wert"]["Beschichtungsabstand Anode quer zur Bahn"] #[mm] Abstand zwischen den Sheets gegen Bahnrichtung
        Schneid_abd_gg_bahnr_K = Zellformat["Wert"]["Beschichtungsabstand Kathode quer zur Bahn"] #[mm] Abstand zwischen den Sheets gegen Bahnrichtung
                
        #Innenabstände der Separatoren
        abstand_separator_huelle = Zellformat["Wert"]["Abstand Separator - Hülle"] #[mm]
        ueberstand_separator_anode = Zellformat["Wert"]["Überstand Separator - Anode"] #[mm]
        ueberstand_anode_kathode = Zellformat["Wert"]["Überstand Anode - Kathode"] #[mm]
        
        #Maße der Sheets
        breite_anode = breite_festhuelle-2*abstand_separator_huelle-2*ueberstand_separator_anode #[mm]
        breite_kathode = breite_festhuelle-2*abstand_separator_huelle-2*ueberstand_separator_anode-2*ueberstand_anode_kathode #[mm]
        laenge_anode = laenge_festhuelle-2*abstand_separator_huelle-2*ueberstand_separator_anode #[mm]
        laenge_kathode = laenge_festhuelle-2*abstand_separator_huelle-2*ueberstand_separator_anode-2*ueberstand_anode_kathode #[mm]
        
        #Flächen der Bestandteile (Sheets)        
        A_KK = flaeche_mit_zellf(breite_kathode,laenge_kathode,breite_kathode_zellf,laenge_kathode_zellf,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_KB = flaeche_ohne_zellf(breite_kathode,laenge_kathode,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_AK = flaeche_mit_zellf(breite_anode,laenge_anode,breite_anode_zellf,laenge_anode_zellf,eckenradius_elektrode) #Fläche Anode [mm²]
        A_AB = flaeche_ohne_zellf(breite_anode,laenge_anode,eckenradius_elektrode) #Fläche Anode [mm²]
        A_Sep = flaeche_mit_zellf(breite_festhuelle-2*abstand_separator_huelle, laenge_festhuelle-2*abstand_separator_huelle, 0, 0, 0)

        l_WHE = C_flsp*A_KB*2/100 #[mAh] Ladung einer Wiederholeinheit (doppelt beschichtete Kathode -> *2)

        #Anzahl der Wiederholeinheiten in der Zelle
        anzahl_WHE = math.floor((hoehe_festhuelle-d_MWHE/1000)/(d_WHE/1000)) #[-], floor is abrunden

        A_AB_ges = A_AB*(anzahl_WHE+1)*2
        A_KB_ges = A_KB*anzahl_WHE*2
        A_AK_ges = A_AK*(anzahl_WHE+1)*2
        A_KK_ges = A_KK*anzahl_WHE*2
        A_Sep_ges = A_Sep*(anzahl_WHE+1)*2


        #Meter Elektrode/Sheet
        #Anzahl Sheets übereinander (beschichtete Bahnen), normal (für Ausnutzungsgrad) und abgerundet & Sheets pro meter Elektrode (S_MA & S_MK)
        #Anode
        bahnen_bes_A_ausn = (Breite_Anodenkollektor-Schneid_abs_aus_A)/(2*(laenge_anode+laenge_anode_zellf)+Schneid_abs_aus_A+Schneid_abd_gg_bahnr_A)
        bahnen_bes_A = math.floor(bahnen_bes_A_ausn)
        bahnen_bes_A_ausn = round(bahnen_bes_A/bahnen_bes_A_ausn,4)*100
        S_MA = 1000/(breite_anode+Schneid_abs_bahnr_A)*bahnen_bes_A*2
        #Kathode
        bahnen_bes_K_ausn = (Breite_Kathodenkollektor-Schneid_abs_aus_K)/(2*(laenge_kathode+laenge_kathode_zellf)+Schneid_abs_aus_K+Schneid_abd_gg_bahnr_K)
        bahnen_bes_K = math.floor(bahnen_bes_K_ausn)
        bahnen_bes_K_ausn = round(bahnen_bes_K/bahnen_bes_K_ausn,4)*100
        S_MK = 1000/(breite_kathode+Schneid_abs_bahnr_K)*bahnen_bes_K*2            
        
        vol_nutz_zelle = breite_festhuelle * laenge_festhuelle * hoehe_festhuelle #[mm³]
        
    
    if Zelltyp == "Rundzelle":
        Wandstärke = Wandstaerke #[mm]
        #Außenmaße der Runzelle
        radius_rundzelle = Zellformat["Wert"]["Radius Rundzelle"]-Wandstärke #[mm]
        hoehe_rundzelle = Zellformat["Wert"]["Höhe Rundzelle"]-2*Wandstärke #[mm]

        A_Huelle = 2*math.pi*radius_rundzelle*hoehe_rundzelle+math.pi*2*radius_rundzelle**2

        #Abl_in_Zelle_A = Zellformat["Wert"]["Länge Ableiter in Zelle Anode"] #[mm]
        #Abl_in_Zelle_K = Zellformat["Wert"]["Länge Ableiter in Zelle Kathode"] #[mm]

        abs_zellwickel_deckel = Zellformat["Wert"]["Abstand Zellwickel - Deckel"] #[mm]
        
        Beschichtungsabstand_Kathode = Zellformat["Wert"]["Beschichtungsabstand Kathode"] #[mm]
        Beschichtungsabstand_Anode = Zellformat["Wert"]["Beschichtungsabstand Anode"] #[mm]

        #Innenabstände der Separatoren
        ueberstand_separator_anode = Zellformat["Wert"]["Überstand Separator - Anode"] #[mm]
        ueberstand_anode_kathode = Zellformat["Wert"]["Überstand Anode - Kathode"] #[mm]

        #Zellableiter
        Abl_in_Zelle_A = ueberstand_separator_anode+Zellformat["Wert"]["Länge Ableiter in Zelle Anode"] #[mm]
        Abl_in_Zelle_K = ueberstand_separator_anode+ueberstand_anode_kathode+Zellformat["Wert"]["Länge Ableiter in Zelle Kathode"] #[mm]
        
        #Weitere Angaben Rundzelle
        sep_wick = Zellformat["Wert"]["Zusatzwicklungen Separator"] #zusätzliche Separatorwicklungen
        r_w = Zellformat["Wert"]["Radius Wickelkern"] #[mm] Radius Wickelkern

        #l_bahn beschreibt die länge des Anoden-Kathodenverbundes ohne Separatorüberstand, also die Anodenlänge
        l_bahn = ((radius_rundzelle-2*sep_wick*d_Sep/1000)**2-(r_w+2*sep_wick*d_Sep/1000)**2)*math.pi/(d_WHE/1000) #[mm]
               
        #Ich gehe davon aus, dass der Ableiter umgeknickt wird und dmenetsprechend keinen Platz benötigt. 
        A_KK = (hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode-2*ueberstand_anode_kathode+Abl_in_Zelle_K)*(l_bahn-2*ueberstand_anode_kathode)
        A_KB = (hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode-2*ueberstand_anode_kathode)*(l_bahn-2*ueberstand_anode_kathode)
        A_AK = (hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode+Abl_in_Zelle_A)*(l_bahn)
        A_AB = (hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode)*(l_bahn)
        
        A_sep_innen = 0
        A_sep_aussen = 0
        for no_wick in range(int(sep_wick)):
            A_sep_innen+=(hoehe_rundzelle-abs_zellwickel_deckel)*2*math.pi*(r_w+(no_wick+0.5)*d_Sep/1000)
            A_sep_aussen+=(hoehe_rundzelle-abs_zellwickel_deckel)*2*math.pi*(radius_rundzelle-(no_wick+0.5) *d_Sep/1000)
            
        A_Sep = l_bahn*(hoehe_rundzelle-abs_zellwickel_deckel)+A_sep_innen+A_sep_aussen #Fläche Separator [mm²]

        l_WHE = C_flsp*A_KB*2/100 #[mAh] Ladung einer Wiederholeinheit (doppelt beschichtete Kathode -> *2)

        anzahl_WHE = 1
        
        A_AB_ges = A_AB*2
        A_KB_ges = A_KB*2
        A_AK_ges = A_AK
        A_KK_ges = A_KK
        A_Sep_ges = A_Sep*2

        #Meter Elektrode/Sheet
        #Anzahl Sheets übereinander (beschichtete Bahnen), normal (für Ausnutzungsgrad) und abgerundet & Sheets pro meter Elektrode (S_MA & S_MK)
        #Anode
        bahnen_bes_A_ausn = (Breite_Anodenkollektor)/(hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode+Beschichtungsabstand_Anode)
        bahnen_bes_A = math.floor(bahnen_bes_A_ausn)
        if (bahnen_bes_A % 2) != 0 and bahnen_bes_A != 1:
            bahnen_bes_A = bahnen_bes_A-1
        bahnen_bes_A_ausn = round(bahnen_bes_A/bahnen_bes_A_ausn,4)*100
        S_MA = 1000/(l_bahn)*bahnen_bes_A

        #Kathode
        bahnen_bes_K_ausn = (Breite_Kathodenkollektor)/(hoehe_rundzelle-abs_zellwickel_deckel-2*ueberstand_separator_anode-2*ueberstand_anode_kathode+Beschichtungsabstand_Kathode)
        bahnen_bes_K = math.floor(bahnen_bes_K_ausn)
        if (bahnen_bes_K % 2) != 0 and bahnen_bes_K != 1:
            bahnen_bes_K = bahnen_bes_K-1
        bahnen_bes_K_ausn = round(bahnen_bes_K/bahnen_bes_K_ausn,4)*100
        S_MK = 1000/(l_bahn-2*ueberstand_anode_kathode)*bahnen_bes_K

        vol_nutz_zelle = math.pi*radius_rundzelle*radius_rundzelle*hoehe_rundzelle #[mm³]
    
    if Zelltyp == "Hardcase gewickelt":
        #Außenmaße der Zelle
        Wandstärke = Wandstaerke #[mm]

        #Abl_in_Zelle_A = Zellformat["Wert"]["Länge Ableiter in Zelle Anode"] #[mm]
        #Abl_in_Zelle_K = Zellformat["Wert"]["Länge Ableiter in Zelle Kathode"] #[mm]

        breite_festhuelle = Zellformat["Wert"]["Breite Festhülle"]-2*Wandstärke #[mm]
        laenge_festhuelle = Zellformat["Wert"]["Länge Festhülle"]-2*Wandstärke #[mm]
        hoehe_festhuelle = Zellformat["Wert"]["Höhe Festhülle"]-2*Wandstärke #[mm]

        A_Huelle = 2*breite_festhuelle*laenge_festhuelle+2*breite_festhuelle*hoehe_festhuelle+2*laenge_festhuelle*hoehe_festhuelle

        Beschichtungsabstand_Kathode = Zellformat["Wert"]["Beschichtungsabstand Kathode"] #[mm]
        Beschichtungsabstand_Anode = Zellformat["Wert"]["Beschichtungsabstand Anode"] #[mm]
        #Innenabstände der Separatoren
        ueberstand_separator_anode = Zellformat["Wert"]["Überstand Separator - Anode"] #[mm]
        ueberstand_anode_kathode = Zellformat["Wert"]["Überstand Anode - Kathode"] #[mm]
        abs_zellwickel_deckel = Zellformat["Wert"]["Abstand Zellwickel - Deckel"] #[mm]
        abs_ableiter_huelle = Zellformat["Wert"]["Abstand Ableiter - Hülle"] #[mm]

        #Zellableiter
        Abl_in_Zelle_A = ueberstand_separator_anode+Zellformat["Wert"]["Länge Ableiter in Zelle Anode"] #[mm]
        Abl_in_Zelle_K = ueberstand_separator_anode+ueberstand_anode_kathode+Zellformat["Wert"]["Länge Ableiter in Zelle Kathode"] #[mm]

        #Weitere Angaben Prismatische Zelle
        sep_wick = Zellformat["Wert"]["Zusatzwicklungen Separator"] #zusätzliche Separatorwicklungen
        r_w = Zellformat["Wert"]["Radius Wickelkern"] #[mm] Radius Wickelkern

        #Anzahl Wicklungen
        Anz_wick = ((laenge_festhuelle-2*r_w)/2-(4*sep_wick*d_Sep/1000))/(d_WHE/1000) #[-]

        #Breite des Wickelkerns
        Breite_Kern = hoehe_festhuelle-4*sep_wick*d_Sep/1000-2*Anz_wick*d_WHE/1000-abs_zellwickel_deckel-2*r_w #[mm]
        
        U_a = 2*math.pi*r_w+2*Breite_Kern #Umfang des Wickelkerns [mm]
        
        U_plus = 2*math.pi*d_WHE/1000 #Zunahme jeder Wicklung [mm]
        
        #l_bahn = (U_a-U_plus)*Anz_wick + U_a #[mm]
        A_wickel_querschnitt = Breite_Kern*2*Anz_wick*d_WHE/1000+( (r_w+2*sep_wick+Anz_wick*d_WHE/1000)**2 - (r_w+2*sep_wick)**2)*math.pi #[mm]
        l_bahn = A_wickel_querschnitt/d_WHE*1000 #[mm]

        #A_KK = (l_bahn-2*ueberstand_anode_kathode)*(breite_festhuelle-2*ueberstand_anode_kathode-2*ueberstand_separator_anode-abs_ableiter_huelle*2)
        #A_KB = (l_bahn-2*ueberstand_anode_kathode)*(breite_festhuelle-2*ueberstand_anode_kathode-2*ueberstand_separator_anode-Abl_in_Zelle_K-abs_ableiter_huelle*2)
        #A_AK = (l_bahn)*(breite_festhuelle-2*ueberstand_separator_anode-abs_ableiter_huelle*2)
        #A_AB = (l_bahn)*(breite_festhuelle-2*ueberstand_separator_anode-Abl_in_Zelle_A-abs_ableiter_huelle*2)

        A_KK = (l_bahn-2*ueberstand_anode_kathode)*(breite_festhuelle-ueberstand_anode_kathode-Abl_in_Zelle_K-abs_ableiter_huelle*2)
        A_KB = (l_bahn-2*ueberstand_anode_kathode)*(breite_festhuelle-ueberstand_anode_kathode-Abl_in_Zelle_K-Abl_in_Zelle_A-abs_ableiter_huelle*2)
        A_AK = (l_bahn)*(breite_festhuelle+ueberstand_anode_kathode-Abl_in_Zelle_K-abs_ableiter_huelle*2)
        A_AB = (l_bahn)*(breite_festhuelle+ueberstand_anode_kathode-Abl_in_Zelle_K-Abl_in_Zelle_A-abs_ableiter_huelle*2)


        #A_Sep = l_bahn*(breite_festhuelle-abs_ableiter_huelle*2)-Abl_in_Zelle_A-Abl_in_Zelle_K+2*ueberstand_separator_anode+2*ueberstand_anode_kathode
        A_Sep = l_bahn*(breite_festhuelle-abs_ableiter_huelle*2-Abl_in_Zelle_A-Abl_in_Zelle_K+2*ueberstand_separator_anode+2*ueberstand_anode_kathode)

        l_WHE = C_flsp*A_KB*2/100 #[mAh] Ladung einer Wiederholeinheit (doppelt beschichtete Kathode -> *2)

        anzahl_WHE = 1
        
        A_AB_ges = A_AB*2
        A_KB_ges = A_KB*2
        A_AK_ges = A_AK
        A_KK_ges = A_KK
        A_Sep_ges = A_Sep*2
              
        #Meter Elektrode/Sheet
        #Anzahl Sheets übereinander (beschichtete Bahnen), normal (für Ausnutzungsgrad) und abgerundet & Sheets pro meter Elektrode (S_MA & S_MK)
        #Anode
        #bahnen_bes_A_ausn = (Breite_Anodenkollektor)/(breite_festhuelle-2*ueberstand_separator_anode+Beschichtungsabstand_Anode-Abl_in_Zelle_A-abs_ableiter_huelle*2)
        bahnen_bes_A_ausn = (Breite_Anodenkollektor)/(breite_festhuelle+ueberstand_anode_kathode-Abl_in_Zelle_K-Abl_in_Zelle_A-abs_ableiter_huelle*2+Beschichtungsabstand_Anode)
        
        bahnen_bes_A = math.floor(bahnen_bes_A_ausn)
        if (bahnen_bes_A % 2) != 0 and bahnen_bes_A != 1:
            bahnen_bes_A = bahnen_bes_A-1
        bahnen_bes_A_ausn = round(bahnen_bes_A/bahnen_bes_A_ausn,4)*100
        S_MA = 1000/(l_bahn)*bahnen_bes_A

        #Kathode
        #bahnen_bes_K_ausn = (Breite_Kathodenkollektor)/(breite_festhuelle-2*ueberstand_separator_anode-2*ueberstand_anode_kathode+Beschichtungsabstand_Kathode-Abl_in_Zelle_K-abs_ableiter_huelle*2)
        bahnen_bes_K_ausn = (Breite_Kathodenkollektor)/(breite_festhuelle-ueberstand_anode_kathode-Abl_in_Zelle_K-Abl_in_Zelle_A-abs_ableiter_huelle*2+Beschichtungsabstand_Kathode)
        
        bahnen_bes_K = math.floor(bahnen_bes_K_ausn)
        if (bahnen_bes_K % 2) != 0 and bahnen_bes_K != 1:
            bahnen_bes_K = bahnen_bes_K-1
        bahnen_bes_K_ausn = round(bahnen_bes_K/bahnen_bes_K_ausn,4)*100
        S_MK = 1000/(l_bahn-2*ueberstand_anode_kathode)*bahnen_bes_K
        
        vol_nutz_zelle = breite_festhuelle * laenge_festhuelle * hoehe_festhuelle #[mm³]
        
 
    #____________________________________
    # Ab hier wieder gesammelte Berechnung für alle Zelltypen
    
    #Gewichte der Einzelsheets jeweils & Gewicht der gesamten WHE
    gew_AK = A_AK*d_AK*roh_AK/1000000 #[g]
    gew_AB = A_AB*d_AB*roh_AB/1000000 #[g], einzeln
    gew_KK = A_KK*d_KK*roh_KK/1000000 #[g]
    gew_KB = A_KB*d_KB*roh_KB/1000000 #[g], einzeln
    gew_Sep = A_Sep*d_Sep*roh_sep/1000000 #[g]
    gew_WHE = gew_AK+2*gew_AB+gew_KK+2*gew_KB+2*gew_Sep
    gew_MWHE = gew_AK+2*gew_AB+2*gew_Sep
    
    #Volumina der Einzelsheets
    vol_sep = A_Sep_ges * d_Sep/1000 #[mm³]
    vol_AB = A_AB * d_AB/1000 #[mm³]
    vol_AK = A_AK * d_AK/1000 #[mm³]
    vol_KB = A_KB * d_KB/1000 #[mm³]
    vol_KK = A_KK * d_KK/1000 #[mm³]
    
    #Volumen und Gewicht des Elektrolyts
    vol_elyt = vol_sep*2 * phi_sep/100 + vol_AB*2 * phi_AB/100 + vol_KB*2 * phi_KB/100 + (vol_nutz_zelle - (vol_sep*2 + vol_AB*2 + vol_AK + vol_KB*2 + vol_KK)*anzahl_WHE)*elektrolytbefuellung/100 #[mm³]
    gew_elyt = vol_elyt*roh_elyt/1000 #[g]

    volumenfaktor = vol_elyt/(vol_sep*2 * phi_sep/100 + vol_AB*2 * phi_AB/100 + vol_KB*2 * phi_KB/100)

    rho_huelle = read_zellinfo(Huelle)["Wert"]["Dichte"] #[g/cm³]
    gew_huelle = A_Huelle*Wandstaerke*rho_huelle/1000
    
    #die Gesamtgewichte der Einzelbestandteile 
    #gewickelte Zellen haben keine modifizierte Wiederholeinheit, gestapelte Zellen schon
    if Zelltyp == "Pouchzelle gestapelt" or Zelltyp == "Hardcase gestapelt":
        gew_AK_ges = gew_AK*(anzahl_WHE+1) #[g] +1 für die modifizierte Wiederholeinheit
        gew_AB_ges = gew_AB*(anzahl_WHE+1)*2 #[g] +1 für die modifizierte Wiederholeinheit, *2 für die doppelseitige Beschichtung 
        gew_KK_ges = gew_KK*anzahl_WHE #[g]
        gew_KB_ges = gew_KB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_Sep_ges = gew_Sep*(anzahl_WHE+1)*2 #[g] +1 für die modifizierte Wiederholeinheit, *2, da eine WHE 2 Separator Blätter enthält
        gew_ges = gew_elyt + gew_WHE*anzahl_WHE + gew_MWHE
    
    if Zelltyp == "Rundzelle" or Zelltyp == "Hardcase gewickelt":
        gew_AK_ges = gew_AK*anzahl_WHE #[g] 
        gew_AB_ges = gew_AB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_KK_ges = gew_KK*anzahl_WHE #[g]
        gew_KB_ges = gew_KB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_Sep_ges = gew_Sep*anzahl_WHE*2 #[g] *2, da eine WHE 2 Separator Blätter enthält
        gew_ges = gew_elyt + gew_WHE * anzahl_WHE
       
    
    #Gesamtladung einer Zelle, Anzahl zu produzierender Zellen/ Jahr, spezifische Ladungsdichte einer Zelle
    Q_ges = l_WHE*anzahl_WHE/1000 #gesamte Ladung einer Zelle in Ah
    Zellen_pro_Jahr = GWh_pro_jahr*1000000000/(Q_ges*U) #*1 Mrd wegen Giga
    spez_energie = U*Q_ges*1000/gew_ges #[Wh/kg] *1000 -> Gewicht Zelle g zu kg
    #Balancing = (1-(A_KB*C_flsp)/(A_AB*C_flsp))*100
    Balancing = (1-(A_KB*C_flsp)/(A_AB*C_flsp))*100

    Kosten_Huelle = read_zellinfo(Huelle)["Wert"]["Preis"] #[€/m²]
    
    #Auflistung aller Kosten einer Zelle
    Gesamtkosten_Anodenbeschichtung = Kosten_Anodenbeschichtung * gew_AB_ges/1000 #[€]
    Gesamtkosten_Kathodenbeschichtung = Kosten_Kathodenbeschichtung * gew_KB_ges/1000 #[€]
    Gesamtkosten_Anodenkollektor = Kosten_Anodenkollektor * A_AK_ges / 1000000 #[€]
    Gesamtkosten_Kathodenkollektor = Kosten_Kathodenkollektor * A_KK_ges / 1000000 #[€]
    Gesamtkosten_Huelle = Kosten_Huelle * A_Huelle /1e6
    Gesamtkosten_Separator = Kosten_Separator * A_Sep_ges / 1000000
    Gesamtkosten_Elektrolyt = Kosten_Elektrolyt * gew_elyt/1000 #[€]
    Gesamtkosten_Zelle = (Gesamtkosten_Anodenbeschichtung 
                        + Gesamtkosten_Kathodenbeschichtung 
                        + Gesamtkosten_Anodenkollektor 
                        + Gesamtkosten_Kathodenkollektor 
                        + Gesamtkosten_Kathodenkollektor
                        + Gesamtkosten_Separator
                        + Gesamtkosten_Elektrolyt
                        )
    
    #____________________________________
    # Ab hier der Export aller Informationen
    

                       
    
    export_zellberechnung = [
        
        {"Beschreibung":"Ladung","Wert":round(Q_ges,2),"Einheit":"Ah","Kategorie":"Übersicht"},
        {"Beschreibung":"Zellformat","Wert":Zellname,"Einheit":"","Kategorie":"Übersicht"},
        {"Beschreibung":"Zelltyp","Wert":Zelltyp,"Einheit":"","Kategorie":"Übersicht"},
        {"Beschreibung":"Nennspannung","Wert":U,"Einheit":"V","Kategorie":"Übersicht"},
        {"Beschreibung":"Energiedichte","Wert":round(spez_energie,2),"Einheit":"WH/kg","Kategorie":"Übersicht"},
        {"Beschreibung":"Zellen pro Jahr","Wert":round(Zellen_pro_Jahr,2),"Einheit":"","Kategorie":"Übersicht"},
        {"Beschreibung":"Gesamtgewicht Zelle","Wert":round(gew_ges,2),"Einheit":"g","Kategorie":"Übersicht"},
        {"Beschreibung":"Volmenfaktor","Wert":round(volumenfaktor,2),"Einheit":"-","Kategorie":"Übersicht"},
        
        #{"Beschreibung":"Balancing","Wert":round(Balancing,2),"Einheit":"%","Kategorie":"Übersicht"},
        
        {"Beschreibung":"Anzahl Wiederholeinheiten","Wert":anzahl_WHE,"Einheit":"","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Fläche Anodenbeschichtung gesamt","Wert":round(A_AB_ges,2),"Einheit":"mm²","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Fläche Kathodenbeschichtung gesamt","Wert":round(A_KB_ges,2),"Einheit":"mm²","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Balancing","Wert":round(Balancing,2),"Einheit":"%","Kategorie":"Maße und Flächen"},
        
        {"Beschreibung":"Gesamtdichte Anodenbeschichtung","Wert":round(Gesamtdichte_Anodenbeschichtung,2),"Einheit":"g/cm³","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gesamtdichte Kathodenbeschichtung","Wert":round(Gesamtdichte_Kathodenbeschichtung,2),"Einheit":"g/cm³","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Anodenkollektor","Wert":round(gew_AK_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Kathodenkollektor","Wert":round(gew_KK_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Anodenbeschichtung","Wert":round(gew_AB_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Kathodenbeschichtung","Wert":round(gew_KB_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Separator","Wert":round(gew_Sep_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Elektrolyt","Wert":round(gew_elyt,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Hülle","Wert":round(gew_huelle,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gesamtgewicht Zelle","Wert":round(gew_ges,2),"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        
        {"Beschreibung":"Kilopreis Anodenbeschichtung","Wert":round(Kosten_Anodenbeschichtung,2),"Einheit":"€/kg","Kategorie":"Kosten"},
        {"Beschreibung":"Kilopreis Kathodenbeschichtung","Wert":round(Kosten_Kathodenbeschichtung,2),"Einheit":"€/kg","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Anodenbeschichtung","Wert":round(Gesamtkosten_Anodenbeschichtung,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Kathodenbeschichtung","Wert":round(Gesamtkosten_Kathodenbeschichtung,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Anodenkollektor","Wert":round(Gesamtkosten_Anodenkollektor,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Kathodenkollektor","Wert":round(Gesamtkosten_Kathodenkollektor,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Separator","Wert":round(Gesamtkosten_Separator,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Elektrolyt","Wert":round(Gesamtkosten_Elektrolyt,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Hülle","Wert":round(Gesamtkosten_Huelle,2),"Einheit":"€","Kategorie":"Kosten"},
        {"Beschreibung":"Materialkosten einer Zelle","Wert":round(Gesamtkosten_Zelle,2),"Einheit":"€","Kategorie":"Kosten"},
        
        {"Beschreibung":"Beschichtete Bahnen Anode Ausnutzung","Wert":bahnen_bes_A_ausn,"Einheit":"%","Kategorie":"Flächennutzung Elektrode"},
        {"Beschreibung":"Beschichtete Bahnen Anode","Wert":bahnen_bes_A,"Einheit":"","Kategorie":"Flächennutzung Elektrode"},
        {"Beschreibung":"Sheets/ Meter Anode","Wert":S_MA,"Einheit":"Sheet/m","Kategorie":"Flächennutzung Elektrode"},
        {"Beschreibung":"Beschichtete Bahnen Kathode Ausnutzung","Wert":bahnen_bes_K_ausn,"Einheit":"%","Kategorie":"Flächennutzung Elektrode"},
        {"Beschreibung":"Beschichtete Bahnen Kathode","Wert":bahnen_bes_K,"Einheit":"","Kategorie":"Flächennutzung Elektrode"},
        {"Beschreibung":"Sheets/ Meter Kathode","Wert":S_MK,"Einheit":"Sheet/m","Kategorie":"Flächennutzung Elektrode"},
            ]
    
    return (pd.DataFrame(export_zellberechnung))



#zellberechnung(Zellchemie, Materialinfos, Zellformat, Weitere_Zellinfos)