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
# 4. Name Zellformat [string]
# 5. Zelltyp [string]
# 6. Gesamtladung einer Zelle (nur Pouchzelle) -> fehlt noch aus dem Frontend
# -> Hülle fehlt noch gesamt    

# Zellchemie_raw = '[{"id":1,"Beschreibung":"NCM 622","Kategorie":"Aktivmaterial Kathode","Wert":97.0,"Einheit":"%"},{"id":2,"Beschreibung":"Graphit","Kategorie":"Aktivmaterial Anode","Wert":96.5,"Einheit":"%"},{"id":3,"Beschreibung":"Kupferfolie 10 \u00b5m","Kategorie":"Kollektorfolie Anode","Wert":null,"Einheit":"%"},{"id":4,"Beschreibung":"Aluminiumfolie 8 \u00b5m","Kategorie":"Kollektorfolie Kathode","Wert":null,"Einheit":"%"},{"id":6,"Beschreibung":"Wasser","Kategorie":"L\u00f6semittel Anode","Wert":3.0,"Einheit":"%"},{"id":10,"Beschreibung":"Zellspannung","Kategorie":"Allgemeine Parameter","Wert":3.7,"Einheit":"V"},{"id":11,"Beschreibung":"Irreversibler Formierungsverlust","Kategorie":"Allgemeine Parameter","Wert":10.0,"Einheit":"%"},{"id":12,"Beschreibung":"Zieldichte Beschichtung Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":3.0,"Einheit":"g\/cm\u00b3"},{"id":13,"Beschreibung":"Beschichtungsporosit\u00e4t Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":25.0,"Einheit":"%"},{"id":14,"Beschreibung":"Fl\u00e4chenspezifische Kapazit\u00e4t Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":4.0,"Einheit":"mAh\/cm\u00b2"},{"id":15,"Beschreibung":"Feststoffgehalt Kathode","Kategorie":"Elektrodenparameter Kathode","Wert":60.0,"Einheit":"%"},{"id":16,"Beschreibung":"Zieldichte Beschichtung Anode","Kategorie":"Elektrodenparameter Anode","Wert":1.6,"Einheit":"g\/cm\u00b3"},{"id":17,"Beschreibung":"Beschichtungsporosit\u00e4t Anode","Kategorie":"Elektrodenparameter Anode","Wert":34.0,"Einheit":"%"},{"id":18,"Beschreibung":"Fl\u00e4chenspezifische Kapazit\u00e4t Anode","Kategorie":"Elektrodenparameter Anode","Wert":3.2,"Einheit":"mAh\/cm\u00b2"},{"id":19,"Beschreibung":"Feststoffgehalt Anode","Kategorie":"Elektrodenparameter Anode","Wert":60.0,"Einheit":"%"},{"id":20,"Beschreibung":"Kalkulierter Anoden\u00fcberschuss","Kategorie":"Elektrodenparameter Anode","Wert":10.0,"Einheit":"%"},{"id":21,"Beschreibung":"NMP","Kategorie":"L\u00f6semittel Kathode","Wert":63.4,"Einheit":"%"},{"id":22,"Beschreibung":"ProZell Separator","Kategorie":"Separator","Wert":null,"Einheit":"%"},{"id":23,"Beschreibung":"K-Leitru\u00df 1","Kategorie":"Additive Kathode","Wert":3.0,"Einheit":"%"},{"id":24,"Beschreibung":"K-Leitru\u00df 2","Kategorie":"Additive Kathode","Wert":0.0,"Einheit":"%"},{"id":25,"Beschreibung":"K-Additiv","Kategorie":"Additive Kathode","Wert":1.0,"Einheit":"%"},{"id":26,"Beschreibung":"K-Binder 1","Kategorie":"Additive Kathode","Wert":3.0,"Einheit":"%"},{"id":27,"Beschreibung":"K-Binder 2","Kategorie":"Additive Kathode","Wert":0.0,"Einheit":"%"},{"id":28,"Beschreibung":"A-Leitru\u00df 1","Kategorie":"Additive Anode","Wert":1.0,"Einheit":"%"},{"id":29,"Beschreibung":"A-Leitru\u00df 2","Kategorie":"Additive Anode","Wert":0.0,"Einheit":"%"},{"id":31,"Beschreibung":"A-Binder 1","Kategorie":"Additive Anode","Wert":1.0,"Einheit":"%"},{"id":32,"Beschreibung":"A-Binder 2","Kategorie":"Additive Anode","Wert":1.5,"Einheit":"%"},{"id":33,"Beschreibung":"1M LiPF6 (EC: EMC 3:7 wt%) + 2 wt% VC","Kategorie":"Elektrolyt","Wert":null,"Einheit":"%"}]'
# Materialinfos_raw = '[{"NCM 622":[{"id":3,"Beschreibung":"spezifische Kapazität","Wert":160,"Einheit":"mAh/g"},{"id":4,"Beschreibung":"Dichte","Wert":0.476,"Einheit":"g/cm³"},{"id":5,"Beschreibung":"Preis","Wert":25.75,"Einheit":"€/kg"}]},{"Graphit":[{"id":1,"Beschreibung":"spezifische Kapazität","Wert":330,"Einheit":"mAh/g"},{"id":2,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Preis","Wert":7.46,"Einheit":"€/kg"}]},{"Kupferfolie 10 µm":[{"id":1,"Beschreibung":"Dicke","Wert":10,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":8.96,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Breite","Wert":600,"Einheit":"mm"},{"id":4,"Beschreibung":"Preis","Wert":0.44,"Einheit":"€/m"}]},{"Aluminiumfolie 8 µm":[{"id":1,"Beschreibung":"Dicke","Wert":8,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":2.7,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Breite","Wert":600,"Einheit":"mm"},{"id":4,"Beschreibung":"Preis","Wert":0.2,"Einheit":"€/m"}]},{"Wasser":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":0.01,"Einheit":"€/kg"}]},{"NMP":[{"id":1,"Beschreibung":"Dichte","Wert":1.2,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":2.39,"Einheit":"€/kg"}]},{"ProZell Separator":[{"id":1,"Beschreibung":"Dicke","Wert":20,"Einheit":"µm"},{"id":2,"Beschreibung":"Dichte","Wert":10,"Einheit":"g/cm³"},{"id":3,"Beschreibung":"Porosität","Wert":40,"Einheit":"%"},{"id":4,"Beschreibung":"Preis","Wert":0.5,"Einheit":"€/m²"}]},{"K-Leitruß 1":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"K-Leitruß 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"K-Additiv":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":10,"Einheit":"€/kg"}]},{"K-Binder 1":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":18,"Einheit":"€/kg"}]},{"K-Binder 2":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":18,"Einheit":"€/kg"}]},{"A-Leitruß 1":[{"id":1,"Beschreibung":"Dichte","Wert":2.25,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"A-Leitruß 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":5.07,"Einheit":"€/kg"}]},{"A-Binder 1":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":1.5,"Einheit":"€/kg"}]},{"A-Binder 2":[{"id":1,"Beschreibung":"Dichte","Wert":1,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":1.5,"Einheit":"€/kg"}]},{"1M LiPF6 (EC: EMC 3:7 wt%) + 2 wt% VC":[{"id":1,"Beschreibung":"Dichte","Wert":1.3,"Einheit":"g/cm³"},{"id":2,"Beschreibung":"Preis","Wert":7.44,"Einheit":"€/kg"}]}]'
# Zellformat_raw = '[{"id":1,"Beschreibung":"Breite Anode","Wert":110.0,"Einheit":"mm"},{"id":2,"Beschreibung":"L\u00e4nge Anode","Wert":150.0,"Einheit":"mm"},{"id":3,"Beschreibung":"Breite Zellf\u00e4hnchen Anode","Wert":22.0,"Einheit":"mm"},{"id":4,"Beschreibung":"L\u00e4nge Zellf\u00e4hnchen Anode","Wert":30.0,"Einheit":"mm"},{"id":5,"Beschreibung":"Breite Kathode","Wert":105.0,"Einheit":"mm"},{"id":6,"Beschreibung":"L\u00e4nge Kathode","Wert":145.0,"Einheit":"mm"},{"id":7,"Beschreibung":"Breite Zellf\u00e4hnchen Kathode","Wert":22.0,"Einheit":"mm"},{"id":8,"Beschreibung":"L\u00e4nge Zellf\u00e4hnchen Kathode","Wert":32.5,"Einheit":"mm"},{"id":9,"Beschreibung":"Eckenradius","Wert":5.0,"Einheit":"mm"},{"id":10,"Beschreibung":"Breite Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":11,"Beschreibung":"L\u00e4nge Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":12,"Beschreibung":"H\u00f6he Festh\u00fclle","Wert":null,"Einheit":"mm"},{"id":13,"Beschreibung":"Radius Rundzelle","Wert":null,"Einheit":"mm"},{"id":14,"Beschreibung":"H\u00f6he Rundzelle","Wert":null,"Einheit":"mm"},{"id":15,"Beschreibung":"Radius Wickelkern","Wert":null,"Einheit":"mm"},{"id":16,"Beschreibung":"Zusatzwicklungen Separator","Wert":null,"Einheit":"[-]"},{"id":17,"Beschreibung":"Abstand Separator - H\u00fclle","Wert":null,"Einheit":"mm"},{"id":18,"Beschreibung":"\u00dcberstand Separator - Anode","Wert":2.0,"Einheit":"mm"},{"id":19,"Beschreibung":"\u00dcberstand Anode - Kathode","Wert":null,"Einheit":"mm"},{"id":20,"Beschreibung":"Unterdruck Zelle","Wert":null,"Einheit":"mbar"},{"id":21,"Beschreibung":"Elektrolytbef\u00fcllung","Wert":60,"Einheit":"%"},{"id":22,"Beschreibung":"Sicherheitsabstand Schneiden","Wert":20.0,"Einheit":"mm"},{"id":23,"Beschreibung":"Beschichtungsabstand Kathode","Wert":20.0,"Einheit":"mm"},{"id":24,"Beschreibung":"Beschichtungsabstand Anode","Wert":20.0,"Einheit":"mm"},{"id":25,"Beschreibung":"Breite Kathodenkollektor","Wert":300.0,"Einheit":"mm"},{"id":26,"Beschreibung":"Breite Anodenkollektor","Wert":300.0,"Einheit":"mm"}]'
# weitere_Zellinfos_raw = '{"id":1,"Beschreibung":"BLB 2 Pouch","Zellformat":"Pouchzelle","Dateiname":"BLB_2_Pouch","Ah_pro_Jahr":"10"}'


def zellberechnung(Zellchemie_raw, Materialinfos_raw, Zellformat_raw, weitere_Zellinfos_raw):
    #____________________________________
    # allgemeine Funktionen
    # Filtert aus der gesammelten Materialinfo Tabelle ein Material heraus und gibt es als df zurück 
    def read_zellinfo(Material):
        df = Materialinfos.loc[Materialinfos["Material"] == Material]
        return df
    
    # flaeche_mit_zellf errechnet die Fäche eines Sheets mit Zellfähnchen, inklusive der Radien
    def flaeche_mit_zellf(breite, laenge, breite_zellf, laenge_zellf, radius):
        return breite*laenge+breite_zellf*laenge_zellf-4*(radius*radius-math.pi*radius*radius/4)
    
    
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
    
    Elektrolyt = Zellchemie.loc[Zellchemie['Kategorie'] == "Elektrolyt"].index[0] #String
    
    #Hülle = Zellchemie.loc[Zellchemie['Kategorie'] == "Hülle"].index[0] #String
    
    #____________________________________
    #Zellchemie Parameter auslegen, gelten für alle Zellparameter
    
    U = Zellchemie["Wert"]["Zellspannung"] #Zellspannung in Volt [V]
    delta_irr = Zellchemie["Wert"]["Irreversibler Formierungsverlust"] #Irreversibler Formierungsverlust in Prozent [%]
    
    d_KK = Materialinfos.loc[Materialinfos["Material"] == Kollektorfolie_Kathode]["Wert"]["Dicke"] #[µm]
    roh_KK = Materialinfos.loc[Materialinfos["Material"] == Kollektorfolie_Kathode]["Wert"]["Dichte"] #[g/cm³]
    C_flsp_K = Zellchemie["Wert"]["Flächenspezifische Kapazität Kathode"] #[mAh/cm²]
    C_sp_K = Materialinfos.loc[Materialinfos["Material"] == Aktivmaterial_Kathode]["Wert"]["spezifische Kapazität"] #[mAh/g]
    roh_KB = Zellchemie["Wert"]["Zieldichte Beschichtung Kathode"] #[g/cm³]
    phi_KB = Zellchemie["Wert"]["Beschichtungsporosität Kathode"] #[%]
    x_PM_K = 100-Zellchemie["Wert"][Aktivmaterial_Kathode] #Masseanteil passiver Komponenten Kathode in Prozent [%]
    
    
    d_AK = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Dicke"] #[µm]   
    roh_AK = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Dichte"] #[g/cm³]
    C_flsp_A = Zellchemie["Wert"]["Flächenspezifische Kapazität Anode"] #[mAh/cm²]
    C_sp_A = read_zellinfo(Aktivmaterial_Anode)["Wert"]["spezifische Kapazität"] #[mAh/g]
    roh_AB = Zellchemie["Wert"]["Zieldichte Beschichtung Anode"] #[g/cm³]
    phi_AB = Zellchemie["Wert"]["Beschichtungsporosität Anode"] #[%]
    x_PM_A = 100-Zellchemie["Wert"][Aktivmaterial_Anode] #Masseanteil passiver Komponenten Anode in Prozent [%]
    #delta_A = Zellchemie["Wert"]["kalkulierter Anodenüberschuss"] #[%]
    delta_A = 10 #[%]
     
    d_Sep = read_zellinfo(Separator)["Wert"]["Dicke"] #[µm]
    roh_sep = read_zellinfo(Separator)["Wert"]["Dichte"] #[g/cm³]
    phi_sep = read_zellinfo(Separator)["Wert"]["Porosität"] #[%]
    
    roh_elyt = read_zellinfo(Elektrolyt)["Wert"]["Dichte"] #[g/cm³]
    
    
    #____________________________________
    #Zusammensetzung der Suspension auslesen, Kosten/ Dichte berechnen
    
    
    Bestandteile_Anodenbeschichtung = Additive_Anode #ohne Lösemittel
    Bestandteile_Anodenbeschichtung.append(Aktivmaterial_Anode) #ohne Lösemittel
    Gesamtdichte_Anodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Anodenbeschichtung)
    Gesamtkosten_Anodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Preis"]*read_zellinfo(x)["Wert"]["Dichte"]/Gesamtdichte_Anodenbeschichtung for x in Bestandteile_Anodenbeschichtung) #€/kg
    Kosten_Anodenkollektor = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Preis"] #[€/m]
    
    
    Bestandteile_Kathodenbeschichtung=Additive_Kathode #ohne Lösemittel
    Bestandteile_Kathodenbeschichtung.append(Aktivmaterial_Kathode) 
    Gesamtdichte_Kathodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Dichte"] for x in Bestandteile_Kathodenbeschichtung)
    Gesamtkosten_Kathodenbeschichtung = sum(Zellchemie["Wert"][x]/100*read_zellinfo(x)["Wert"]["Preis"]*read_zellinfo(x)["Wert"]["Dichte"]/Gesamtdichte_Kathodenbeschichtung for x in Bestandteile_Kathodenbeschichtung) #€/kg
    Kosten_Kathodenkollektor = read_zellinfo(Kollektorfolie_Kathode)["Wert"]["Preis"] #[€/m]
    
            
    Kosten_Separator = read_zellinfo(Separator)["Wert"]["Preis"] #[€/m]
    Kosten_Elektrolyt = read_zellinfo(Elektrolyt)["Wert"]["Preis"] #[€/kg]
            
    #GWh_pro_jahr = float(massemodell_eingaben["GWH_pro_jahr"]) #[-]
    GWh_pro_jahr = weitere_Zellinfos[0]["GWh_pro_jahr"] #[-]
    
    
    #____________________________________
    # Elektrochemische Charakterisierung, gleich für alle Zelltypen
    
    MB_K = C_flsp_K*(1+delta_irr/100)/(C_sp_K*(1-x_PM_K/100)) #Massenbelegung Kathode [g/cm²]
    MB_A = C_flsp_A*(1+delta_irr/100+delta_A/100)/(C_sp_A*(1-x_PM_A/100)) #Massenbelegung Anode [g/cm²]
    
    d_KB = (MB_K/roh_KB)*10000 #Dicke Kathodenbeschichtung [µm]
    d_AB = (MB_A/roh_AB)*10000 #Dicke Anodenbeschichtung [µm]
    d_WHE = d_AK + 2*d_AB + d_KK + 2*d_KB + 2*d_Sep #Dicke einer Wiederholeinheit [µm]
    d_MWHE = d_AK + 2*d_AB + 2*d_Sep #Dicke modifizierte Wiederholeinheit [µm]
    
    
    #____________________________________
            #Zellmaße die für alle Zellen gelten
    eckenradius_elektrode = Zellformat["Wert"]["Eckenradius"] #[mm]
    
    elektrolytbefuellung = Zellformat["Wert"]["Elektrolytbefüllung"] #[%]
    
    Sicherheitsabstand_schneiden = Zellformat["Wert"]["Sicherheitsabstand Schneiden"] #[mm]
    Beschichtungsabstand_Kathode = Zellformat["Wert"]["Beschichtungsabstand Kathode"] #[mm]
    Beschichtungsabstand_Anode = Zellformat["Wert"]["Beschichtungsabstand Anode"] #[mm]
    Breite_Kathodenkollektor = read_zellinfo(Kollektorfolie_Kathode)["Wert"]["Breite"] #[mm]
    Breite_Anodenkollektor = read_zellinfo(Kollektorfolie_Anode)["Wert"]["Breite"] #[mm]
    
    
    
    #____________________________________
    # Ab hier die Berechnung der einzelnen Zelltypen
    if Zelltyp == "Pouchzelle":
        Ah_pro_zelle = weitere_Zellinfos[0]["Ah_pro_Zelle"] #[Ah]
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
        
        #Überstand Separator über die Anode, für die Flächenberechnung des Separators
        ueberstand_separator_anode = Zellformat["Wert"]["Überstand Separator - Anode"] #[mm]
    
        #Flächen der Bestandteile (Sheets)
        A_KK = flaeche_mit_zellf(breite_kathode,laenge_kathode,breite_kathode_zellf,laenge_kathode_zellf,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_KB = flaeche_mit_zellf(breite_kathode,laenge_kathode,0,0,eckenradius_elektrode) #Fläche Kathode [mm²]
        A_AK = flaeche_mit_zellf(breite_anode,laenge_anode,breite_anode_zellf,laenge_anode_zellf,eckenradius_elektrode) #Fläche Anode [mm²]
        A_AB = flaeche_mit_zellf(breite_anode,laenge_anode,0,0,eckenradius_elektrode) #Fläche Anode [mm²]
        A_Sep = flaeche_mit_zellf(breite_anode+2*ueberstand_separator_anode,laenge_anode+2*ueberstand_separator_anode,0,0, eckenradius_elektrode) #Fläche Separator [mm²]
    
        
        l_WHE = C_flsp_K*A_KB*2/100 #[mAh] Ladung einer Wiederholeinheit (doppelt beschichtete Kathode -> *2)
    
        #Anzahl der Wiederholeinheiten um auf die gesetzte Ah zu kommen, nach oben aufgerundet
        anzahl_WHE = math.ceil(Ah_pro_zelle*1000/l_WHE)
        
        A_KB_ges = A_KB*anzahl_WHE*2
        A_AB_ges = A_AB*(anzahl_WHE+1)*2
        
        laenge_sheet_kathode = laenge_kathode #[mm]
        breite_sheet_kathode = breite_kathode #[mm]
    
        laenge_sheet_anode = laenge_anode #[mm]
        breite_sheet_anode = breite_anode #[mm]
        
        #nutzbarere Innenraum der Zelle, Fläche des Separators * Höhe des desammten Stacks + die modifizierte WHE
        vol_nutz_zelle = A_Sep * (math.ceil(anzahl_WHE) * d_WHE/1000 + d_MWHE/1000) #[mm³]
     
    
    if Zelltyp == "Hardcase":
        pass 
    
    if Zelltyp == "Rundzelle":
        pass 
    
    if Zelltyp == "Prismatisch":
        pass 
    
    #____________________________________
    # Ab hier wieder gesammelte Berechnung für alle Zelltypen
    
    #Gewichte der Einzelsheets jeweils & Gewicht der gesamten WHE
    gew_AK = A_AK*d_AK*roh_AK/1000000 #[g]
    gew_AB = A_AB*d_AB*roh_AB/1000000 #[g], einzeln
    gew_KK = A_KK*d_KK*roh_KK/1000000 #[g]
    gew_KB = A_KB*d_KB*roh_KB/1000000 #[g], einzeln
    gew_Sep = A_Sep*d_Sep*roh_sep/1000000 #[g]
    gew_MWHE = gew_AK+2*gew_AB+gew_KK+2*gew_KB+2*gew_Sep
    gew_WHE = gew_AK+2*gew_AB+2*gew_Sep
    
    #Volumina der Einzelsheets
    vol_sep = A_Sep * d_Sep/1000 #[mm³]
    vol_AB = A_AB * d_AB/1000 #[mm³]
    vol_AK = A_AK * d_AK/1000 #[mm³]
    vol_KB = A_KB * d_KB/1000 #[mm³]
    vol_KK = A_KK * d_KK/1000 #[mm³]
    
    #Volumen und Gewicht des Elektrolyts
    vol_elyt = vol_sep * phi_sep/100 + vol_AB * phi_AB/100 + vol_KB * phi_KB/100 + (vol_nutz_zelle - (vol_sep + vol_AB + vol_AK + vol_KB + vol_KK)*anzahl_WHE)*elektrolytbefuellung/100 #[mm³]
    gew_elyt = vol_elyt*roh_elyt/1000 #[g]
    
    #die Gesamtgewichte der Einzelbestandteile 
    #gewickelte Zellen haben keine modifizierte Wiederholeinheit, gestapelte Zellen schon
    if Zelltyp == "Pouchzelle" or Zelltyp == "Hardcase":
        gew_AK_ges = gew_AK*(anzahl_WHE+1) #[g] +1 für die modifizierte Wiederholeinheit
        gew_AB_ges = gew_AB*(anzahl_WHE+1)*2 #[g] +1 für die modifizierte Wiederholeinheit, *2 für die doppelseitige Beschichtung 
        gew_KK_ges = gew_KK*anzahl_WHE #[g]
        gew_KB_ges = gew_KB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_Sep_ges = gew_Sep*(anzahl_WHE+1)*2 #[g] +1 für die modifizierte Wiederholeinheit, *2, da eine WHE 2 Separator Blätter enthält
        gew_ges = gew_elyt + gew_WHE*anzahl_WHE + gew_WHE
    
    if Zelltyp == "Rundzelle" or Zelltyp == "Prismatisch":
        gew_AK_ges = gew_AK*anzahl_WHE #[g] 
        gew_AB_ges = gew_AB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_KK_ges = gew_KK*anzahl_WHE #[g]
        gew_KB_ges = gew_KB*anzahl_WHE*2 #[g] *2 für die doppelseitige Beschichtung 
        gew_Sep_ges = gew_Sep*anzahl_WHE*2 #[g] *2, da eine WHE 2 Separator Blätter enthält
        gew_ges = gew_elyt + gew_WHE * anzahl_WHE
       
    
    #Gesamtladung einer Zelle, Anzahl zu produzierender Zellen/ Jahr, spezifische Ladungsdichte einer Zelle
    Q_ges = l_WHE*anzahl_WHE/1000 #gesamte Ladung einer Zelle in Ah
    Zellen_pro_Jahr = GWh_pro_jahr*1000000000/(Q_ges*U) #*1 Mrd wegen Giga
    spez_energie = U*l_WHE*anzahl_WHE/gew_ges
    
    #____________________________________
    # Ab hier der Export aller Informationen
    
    
    # print(Zellchemie)
    # print(Materialinfos)
    # print(Zellformat)
    
    export_zellberechnung = [
        
        {"Beschreibung":"Ladung","Wert":Q_ges,"Einheit":"Ah","Kategorie":"Übersicht"},
        {"Beschreibung":"Zellformat","Wert":Zellname,"Einheit":"","Kategorie":"Übersicht"},
        {"Beschreibung":"Nennspannung","Wert":U,"Einheit":"V","Kategorie":"Übersicht"},
        {"Beschreibung":"Energiedichte","Wert":spez_energie,"Einheit":"WH/kg","Kategorie":"Übersicht"},
        {"Beschreibung":"Zellen pro Jahr","Wert":Zellen_pro_Jahr,"Einheit":"","Kategorie":"Übersicht"},
        {"Beschreibung":"Gesamtgewicht Zelle","Wert":gew_ges,"Einheit":"g","Kategorie":"Übersicht"},
        {"Beschreibung":"Balancing","Wert":0,"Einheit":"%","Kategorie":"Übersicht"},
        
        {"Beschreibung":"Anzahl Wiederholeinheiten","Wert":anzahl_WHE,"Einheit":"","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Fläche Anodenbeschichtung gesamt","Wert":A_KB_ges,"Einheit":"mm²","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Fläche Kathodenbeschichtung gesamt","Wert":A_AB_ges,"Einheit":"mm²","Kategorie":"Maße und Flächen"},
        {"Beschreibung":"Balancing","Wert":0,"Einheit":"%","Kategorie":"Maße und Flächen"},
        
        {"Beschreibung":"Gesamtdichte Anodenbeschichtung","Wert":Gesamtdichte_Anodenbeschichtung,"Einheit":"g/cm³","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gesamtdichte Kathodenbeschichtung","Wert":Gesamtdichte_Kathodenbeschichtung,"Einheit":"g/cm³","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Anodenkollektor","Wert":gew_AK_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Kathodenkollektor","Wert":gew_KK_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Anodenbeschichtung","Wert":gew_AB_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Kathodenbeschichtung","Wert":gew_KB_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Separator","Wert":gew_Sep_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Elektrolyt","Wert":gew_elyt,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gewicht Hülle","Wert":0,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        {"Beschreibung":"Gesamtgewicht Zelle","Wert":gew_ges,"Einheit":"g","Kategorie":"Gewichte und Dichten"},
        
        {"Beschreibung":"Preis Anodenbeschichtung","Wert":Gesamtkosten_Anodenbeschichtung,"Einheit":"€/kg","Kategorie":"Kosten"},
        {"Beschreibung":"Preis Kathodenbeschichtung","Wert":Gesamtkosten_Kathodenbeschichtung,"Einheit":"€/kg","Kategorie":"Kosten"},
        {"Beschreibung":"Materialkosten einer Zelle","Wert":0,"Einheit":"€","Kategorie":"Kosten"},
    
            ]
    
    
    return (pd.DataFrame(export_zellberechnung))

#zellberechnung(Zellchemie_raw, Materialinfos_raw, Zellformat_raw, weitere_Zellinfos_raw)