# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:08:39 2021

@author: bendzuck
"""
import pandas as pd
import math

#____________________________________
#HARDCODED WERTE, BITTE ANPASSEN
arbeitstage_pro_jahr=365
meter_anodenkollektorfolie_pro_rolle=1000
meter_kathodenkollektorfolie_pro_rolle=1000

#____________________________________
#Allgemeine Funktionen

# Wenn vom vorherigen Schritt "neu hinzugefügte Materialien" übergeben werden, werden diese in diesem Schritt auf 0 gesetzt
# Zunächst werden die übergebenen vom str mit ";" getrennt in liste umgewandelt 
def neue_materialien_zu_liste(neue_materialen):
    liste = neue_materialen.split(';')
    return liste
# hier wird die Liste der vormals neuen Materialien durchgegange und auf 0 gesetzt
def materialien_null_setzen(neue_materialen_liste,dictionary):
    if neue_materialen_liste == [""]:
        return dictionary
    else:
        for material in neue_materialen_liste:
            dictionary[material]=0
        return dictionary

def anzahl_sheets_anode(Massemodell_ergebnis):
    if Massemodell_ergebnis["Zellformat"][0]=="Rundzelle":
        anzahl_sheets_anode = Massemodell_ergebnis["Anzahl Wiederholeinheiten"][0]
    else: 
        anzahl_sheets_anode = Massemodell_ergebnis["Anzahl Wiederholeinheiten"][0]+1
    return anzahl_sheets_anode

def anzahl_sheets_kathode(Massemodell_ergebnis):
    anzahl_sheets_kathode = Massemodell_ergebnis["Anzahl Wiederholeinheiten"][0]
    return anzahl_sheets_kathode

#____________________________________
#Prozessfunktionen
            
def Mischen(df,Zellergebnisse,schritt_dictionary):

    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)

    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    
    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])+float(df["Wert"]["Investition einmalig"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Energiebedarf = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
   
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])
        
    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Anodenbeschichtung;Kathodenbeschichtung"
                }
    materialien_null_setzen(liste,schritt_dictionary)
    return schritt_dictionary
    
def Trockenbeschichten(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Beschichten(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Beschichten_und_Trocknen(df,Zellergebnisse,schritt_dictionary):

    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)

    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    "Sheets/Meter Anodenkollektor"

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
    Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)
    
    Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/float(df["Wert"]["Beschichtungsgeschwindigkeit Anode"]))
    Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/float(df["Wert"]["Beschichtungsgeschwindigkeit Kathode"]))

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode

    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition Anlage"])
    
    Energiebedarf_Anode = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"]))*24*arbeitstage_pro_jahr #[kWh]
    Energiebedarf_Kathode = (Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr #[kWh]
    
    Energiebedarf = Energiebedarf_Anode+Energiebedarf_Kathode #[kWh]
    
    Trocknerlänge_Anode = float(df["Wert"]["Beschichtungsgeschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Beschichtungsgeschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = 3*(2+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = 3*(2+Trocknerlänge_Kathode) #[m2]
    
    Flächenbedarf = Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode #[m²]
   
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])
    
    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,      
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,  
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Anodenkollektor;Kathodenkollektor"
                }
    materialien_null_setzen(liste,schritt_dictionary)
    return schritt_dictionary

def Trocknen(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Prälithiierung(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Kalandrieren(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]*Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]*Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Anlagen_Anode = math.ceil((Meter_Anode_pro_Tag/(24*60))/float(df["Wert"]["Geschw. Anode"]))
    Anlagen_Kathode = math.ceil((Meter_Kathode_pro_Tag/(24*60))/float(df["Wert"]["Geschw. Kathode"]))
    
    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    Investition = Anzahl_Anlagen*df["Wert"]["Investition"]
    Flächenbedarf = Anzahl_Anlagen*df["Wert"]["Anlagengrundfläche"]
    Energiebedarf = Anzahl_Anlagen*df["Wert"]["Leistungsaufnahme"]*24*arbeitstage_pro_jahr   
    FA = Anzahl_Anlagen*df["Wert"]["FA"]
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,       
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }
    materialien_null_setzen(liste,schritt_dictionary)
    return schritt_dictionary
    
def Strukturierung(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Längsschneiden(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]*Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]*Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Anlagen_Anode = math.ceil((Meter_Anode_pro_Tag/(24*60))/float(df["Wert"]["Geschwindigkeit"]))
    Anlagen_Kathode = math.ceil((Meter_Kathode_pro_Tag/(24*60))/float(df["Wert"]["Geschwindigkeit"]))
    
    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    Investition = Anzahl_Anlagen*df["Wert"]["Investitionen"]
    Flächenbedarf = Anzahl_Anlagen*df["Wert"]["Anlagengrundfläche"]
    Energiebedarf = Anzahl_Anlagen*df["Wert"]["Leistungsaufnahme"]*24*arbeitstage_pro_jahr   
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])
    
    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Intensivtrocknen(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Vereinzeln(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Zusatzverlust_Anodenkollektor=float(df["Wert"]["Fixausschuss"])/meter_anodenkollektorfolie_pro_rolle
    Zusatzverlust_Kathodenkollektor=float(df["Wert"]["Fixausschuss"])/meter_kathodenkollektorfolie_pro_rolle
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*(Verlust+Zusatzverlust_Anodenkollektor/100)
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*(Verlust+Zusatzverlust_Kathodenkollektor/100)
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Anodensheets_pro_tag = Zelläquivalent*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/365
    Kathodensheets_pro_tag = Zelläquivalent*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/365
    
    Anodensheets_pro_minute = Anodensheets_pro_tag/(24*60)
    Kathodensheets_pro_minute = Kathodensheets_pro_tag/(24*60)
    
    Anzahl_Anlagen_Anode = math.ceil(Anodensheets_pro_minute/float(df["Wert"]["Geschwindigkeit"]))
    Anzahl_Anlagen_Kathode = math.ceil(Kathodensheets_pro_minute/float(df["Wert"]["Geschwindigkeit"]))
    
    Anzahl_Anlagen = Anzahl_Anlagen_Anode + Anzahl_Anlagen_Kathode

    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    FA = 0
    HiK = 0
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])        
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }      
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Laminieren(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Stapeln(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]

    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    
    Zeit_pro_Zelle = (Zellergebnisse["Wert"]['Anzahl Wiederholeinheiten']+1)/float(df["Wert"]["Geschwindigkeit"])+float(df["Wert"]["Zeitverlust Stapelwechsel"])
    Anzahl_Anlagen = math.ceil(Zellen_pro_Tag/(24*60*60/Zeit_pro_Zelle))
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        #"Separator":0,

        "Separator":Separator,

        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Separator"
                }
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Wickeln_Z_Falten(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Wickeln(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]   
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    
    Länge_Wickel = 3000 #[mm]
    
    Zeit_einer_Zelle = Länge_Wickel/1000/df["Wert"]["Geschwindigkeit"]*60 + df["Wert"]["Zeitverlust Wickelwechsel"] #[s]
    Kapazität_pro_Tag = 24*60*60/Zeit_einer_Zelle
    
    Anzahl_Anlagen = math.ceil(Zellen_pro_Tag/Kapazität_pro_Tag)
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }                    
    materialien_null_setzen(liste,schritt_dictionary)    

    return schritt_dictionary

def Kontaktieren(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Anzahl_Anlagen = math.ceil(Zellen_pro_Minute/float(df["Wert"]["Geschwindigkeit"]))
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])   

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }                    
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Assemblieren(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Anzahl_Anlagen = math.ceil(Zellen_pro_Minute/float(df["Wert"]["Geschwindigkeit"]))
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])   

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }                
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Pouchbeutel___Gehäuse_verschließen(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Anzahl_Anlagen = math.ceil(Zellen_pro_Minute/float(df["Wert"]["Geschwindigkeit"]))
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])   

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }            
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Elektrolyt_dosieren(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]*Verlust
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Durchsatz_pro_Minute = 60*float(df["Wert"]["Parallelbefüllungen"])/float(df["Wert"]["Befülldauer je Zelle"])
    Anzahl_Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])        
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        #"Elektrolyt":0,
        "Neue Materialien":"Elektrolyt",
        
        "Elektrolyt":Elektrolyt        
        
                }        
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Befüllöffnung_verschließen(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]*Verlust
   
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60)
    Anzahl_Anlagen = math.ceil(Zellen_pro_Minute/float(df["Wert"]["Geschwindigkeit"]))
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investitionen"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*arbeitstage_pro_jahr*24
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])    

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }    
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Formieren(df,Zellergebnisse,schritt_dictionary):
      
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]*Verlust
  
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Module = math.ceil(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz"]))
    Bediengeräte = math.ceil(float(Zellen_pro_Tag/50000))
    Investition=Module*float(df["Wert"]["Investition Modul"])+Bediengeräte*float(df["Wert"]["Investition Bediengerät"])
    Flächenbedarf=Module*float(df["Wert"]["Anlagengrundfläche"])/10
    
    
    Q_Z=float(Zellergebnisse["Wert"]["Ladung"]) #Speicherkapazität der Batteriezelle [Ah]
    U_OCV=float(Zellergebnisse["Wert"]["Nennspannung"]) #Klemmspannung [Volt]
    Eta_C1=float(df["Wert"]["Eta C1"]) #Coulombscher Wirkungsgrad des ersten Ladezyklus [-]
    Eta_Z=float(df["Wert"]["Eta Z"]) #Wirkungsgrad der Zelle [-]
    
    E_L1=Q_Z*U_OCV/(Eta_C1*Eta_Z) #Energiebedarf des 1. Ladevorgangs [Wh]
    E_E1=Q_Z*U_OCV*Eta_Z #Energiebedarf des 1. Entladevorgangs [Wh]
    E_L2=Q_Z*U_OCV/Eta_Z #Energiebedarf des 2. Ladevorgangs [Wh]
    E_E2=Q_Z*U_OCV*Eta_Z #Energiebedarf des 2. Entladevorgangs [Wh]
    E_L50=0.5*Q_Z*U_OCV/Eta_Z #Energiebedarf des letzten Ladevorgangs auf 50% SOC [Wh]
    E_FormZ=E_L1-E_E1+E_L2-E_E2+E_L50 #Energiebedarf Formierung einer Zelle [Wh]
    
    Energiebedarf=E_FormZ*Zelläquivalent/1000 #[kWh]
    
    FA=float(df["Wert"]["FA"])
    HiK=float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])        
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }
    materialien_null_setzen(liste,schritt_dictionary)
    return schritt_dictionary
    
def Reifelagern(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust  
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]*Verlust
    
    
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    
    Anzahl_Anlagen = 1
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition Bediengerät"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    FA = float(df["Wert"]["FA"])
    HiK = float(df["Wert"]["HiK"])    

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])        
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }    
    materialien_null_setzen(liste,schritt_dictionary)    
    return schritt_dictionary

def Prüfen_und_Klassifizieren(df,Zellergebnisse,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)
    
    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]*Verlust
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]*Verlust
    Elektrolyt=schritt_dictionary["Elektrolyt"]*Verlust
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    Anzahl_Anlagen = math.ceil(Zellen_pro_Tag/(float(df["Wert"]["Durchsatz"])*24))
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Energie"])*24*arbeitstage_pro_jahr
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":""
                }
    materialien_null_setzen(liste,schritt_dictionary)
    return schritt_dictionary



#_____________________________________________________________________________
#neue ProZell Schritte
def MultiEx_Mischen(df,Zellergebnisse,schritt_dictionary):
    Verlust = (1+float(df["Wert"]["variabler Ausschuss"])/100)

    Zelläquivalent=float(schritt_dictionary["Zelläquivalent"])*Verlust
    
    Anodenkollektor=schritt_dictionary["Anodenkollektor"]
    Kathodenkollektor=schritt_dictionary["Anodenkollektor"]
    Anodenbeschichtung=schritt_dictionary["Anodenbeschichtung"]*Verlust
    Kathodenbeschichtung=schritt_dictionary["Kathodenbeschichtung"]*Verlust
    Separator=schritt_dictionary["Separator"]
    Elektrolyt=schritt_dictionary["Elektrolyt"]
    
    Zellen_pro_Tag = Zelläquivalent/arbeitstage_pro_jahr
    
    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Dichte Anodenbeschichtung"]/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Dichte Kathodenbeschichtung"]/1000 #[l]

    Anlagen_Anode = math.ceil(Liter_Anode_pro_Tag/24/df["Wert"]["Geschwindigkeit"])
    Anlagen_Kathode = math.ceil(Liter_Kathode_pro_Tag/24/df["Wert"]["Geschwindigkeit"])

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Energiebedarf = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
   
    FA = Anzahl_Anlagen*float(df["Wert"]["FA"])
    HiK = Anzahl_Anlagen*float(df["Wert"]["HiK"])
        
    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":0,
        "FA-Personalbedarf (pro Schicht)":FA,
        "HiK-Personalbedarf (pro Schicht)":HiK,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Anodenbeschichtung;Kathodenbeschichtung"
                }
    materialien_null_setzen(liste,schritt_dictionary)
    
    
    
    return schritt_dictionary

def MiKal_Mischen(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def OptiEx(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def ÖkoTroP_Bürstenauftrag(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def ÖkoTroP_Elektrostatisch(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def HighStructures_Extrusion(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def HighStructures_Laser(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Epic(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def RollBatt(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def PräLi_Li_Salz(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def PräLi_PVD(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def PräLi_Opferanode(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def HoLiB_Vereinzeln(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def E_Qual(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def ProfiStruk_Strukturierung(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def HoLiB_Stapeln(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def Cell_Fill(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary

def FormEl(df,Zellergebnisse,schritt_dictionary):
    return schritt_dictionary