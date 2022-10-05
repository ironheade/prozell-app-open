# -*- coding: utf-8 -*-iebs
"""
Created on Wed Feb 24 10:08:39 2021

@author: bendzuck
"""

import math

#____________________________________
#HARDCODED WERTE, BITTE ANPASSEN
arbeitstage_pro_jahr=365

#____________________________________
#Klassen

class basis_prozessschritt:
    def __init__(self,df,Zellergebnisse,Zellchemie,Materialinfos):
        self.df = df
        self.Zellergebnisse = Zellergebnisse
        self.Zellchemie = Zellchemie
        self.Materialinfos = Materialinfos
            
    def variabler_aussschuss(self,dictionary):
        dictionary["Zelläquivalent"]        = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Zelläquivalent"] #[-]
        dictionary["Anodenkollektor"]       = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Anodenkollektor"] #[m]
        dictionary["Kathodenkollektor"]     = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Kathodenkollektor"] #[m]
        dictionary["Anodenbeschichtung"]    = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Anodenbeschichtung"] #[kg]
        dictionary["Kathodenbeschichtung"]  = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Kathodenbeschichtung"] #[kg]
        dictionary["Separator"]             = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Separator"] #[m]
        dictionary["Elektrolyt"]            = (1+self.df["Wert"]["Variabler Ausschuss"]/100)*dictionary["Elektrolyt"] #[l]
        
        return dictionary

    def mitarbeiter_anlagen(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   (self.Anlagen_Anode+self.Anlagen_Kathode)*self.df["Wert"]["Personal Facharbeiter"] #[-]
        dictionary["Personalbedarf Hilfskraft"]     =   (self.Anlagen_Anode+self.Anlagen_Kathode)*self.df["Wert"]["Personal Hilfskräfte"] #[-]
        
        return dictionary
    
    def mitarbeiter_schicht(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   self.df["Wert"]["Personal Facharbeiter"] #[-]
        dictionary["Personalbedarf Hilfskraft"]     =   self.df["Wert"]["Personal Hilfskräfte"] #[-]
        
        return dictionary
        
    def flaechen(self,dictionary):
        dictionary["Flächenbedarf"]             =   (self.Anlagen_Anode+self.Anlagen_Kathode)*self.df["Wert"]["Anlagengrundfläche"] #[m²]
        dictionary["Flächenbedarf Trockenraum"] =   (self.Anlagen_Anode+self.Anlagen_Kathode)*self.df["Wert"]["Anlagengrundfläche Trockenraum"] #[m²]
        
        return dictionary
            
    def energie(self,dictionary):
        dictionary["Energiebedarf"] =   (self.Anlagen_Anode*self.df["Wert"]["Leistungsaufnahme Anode"]+\
                                        self.Anlagen_Kathode*self.df["Wert"]["Leistungsaufnahme Kathode"])*24*365 #[kWh]
        return dictionary
    
    def investition(self,dictionary):
        dictionary["Investition"] = self.Anlagen_Anode*self.df["Wert"]["Investition Anode"] + self.Anlagen_Kathode*self.df["Wert"]["Investition Kathode"] #[€]
        return dictionary
    
    def neue_materialien(self,dictionary,neue_materialien=""):
        neue_materialen_liste = dictionary["Neue Materialien"].split(';')
        if neue_materialen_liste != [""]:
            for material in neue_materialen_liste:
                dictionary[material]=0
            dictionary["Neue Materialien"] = neue_materialien
            return dictionary
        else:
            dictionary["Neue Materialien"] = neue_materialien
            return dictionary
#____________________________________
#Prozessschritte für Suspensionen
class suspension_prozessschritt(basis_prozessschritt):
    def fixausschuss(self,dictionary):

        return dictionary

#____________________________________
#Prozessschritte für Rolle-zu-Rolle Prozesse
class coil_prozessschritt(basis_prozessschritt):
    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/365

        Meter_Anode_pro_Tag = Zellen_pro_Tag*self.Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/self.Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
        Meter_Kathode_pro_Tag = Zellen_pro_Tag*self.Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/self.Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

        Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
        Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)
        
        Anodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
        meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        Kathodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]
        meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        
        Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/float(self.df["Wert"]["Geschwindigkeit Anode"]) #[min]
        Verlust_durch_Nebenzeit_Anode = self.df["Wert"]["Nebenzeiten Anode"]/Zeit_pro_Coil_Anode #[%]
        
        Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/float(self.df["Wert"]["Geschwindigkeit Kathode"])
        Verlust_durch_Nebenzeit_Kathode = float(self.df["Wert"]["Nebenzeiten Kathode"])/Zeit_pro_Coil_Kathode #[%]
        
        Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/float(self.df["Wert"]["Geschwindigkeit Anode"])*(1+Verlust_durch_Nebenzeit_Anode))
        Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/float(self.df["Wert"]["Geschwindigkeit Kathode"])*(1+Verlust_durch_Nebenzeit_Kathode))

        Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

        self.Anlagen_Anode = Anlagen_Anode
        self.Anlagen_Kathode = Anlagen_Kathode

        dictionary["Anzahl Maschinen"] = Anz_Maschinen

        return dictionary
    
    #Fixausschuss pro Coil
    def fixausschuss(self,dictionary):       
        Anodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
        meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        Kathodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]
        meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        
        Zusatzverlust_Anode = self.df["Wert"]["Fixausschuss"]/meter_anodenkollektorfolie_pro_rolle
        Zusatzverlust_Kathode = self.df["Wert"]["Fixausschuss"]/meter_kathodenkollektorfolie_pro_rolle
        
        Zusatzverlust = (Zusatzverlust_Anode+Zusatzverlust_Kathode)/2
        
        dictionary["Zelläquivalent"]        = (1+Zusatzverlust)*dictionary["Zelläquivalent"]
        dictionary["Anodenkollektor"]       = (1+Zusatzverlust_Anode)*dictionary["Anodenkollektor"]
        dictionary["Kathodenkollektor"]     = (1+Zusatzverlust_Kathode)*dictionary["Kathodenkollektor"]
        dictionary["Anodenbeschichtung"]    = (1+Zusatzverlust_Anode)*dictionary["Anodenbeschichtung"]
        dictionary["Kathodenbeschichtung"]  = (1+Zusatzverlust_Kathode)*dictionary["Kathodenbeschichtung"]
        dictionary["Separator"]             = (1+Zusatzverlust)*dictionary["Separator"]
        dictionary["Elektrolyt"]            = (1+Zusatzverlust)*dictionary["Elektrolyt"]
        
        return dictionary
    
#____________________________________
#Prozessschritte für Elektrodenblätter     
class sheet_prozessschritt(basis_prozessschritt):
    def fixausschuss(self,dictionary):
        WHE_pro_tag = dictionary["Zelläquivalent"]/365*(self.Zellergebnisse["Wert"]['Anzahl Wiederholeinheiten'])
        sheet_pro_tag = WHE_pro_tag*2
        Fixausschuss = self.df["Wert"]["Fixausschuss"]#Stk./d
        
        Zusatzverlust = Fixausschuss/sheet_pro_tag      
        
        dictionary["Zelläquivalent"]        = (1+Zusatzverlust)*dictionary["Zelläquivalent"]
        dictionary["Anodenkollektor"]       = (1+Zusatzverlust)*dictionary["Anodenkollektor"]
        dictionary["Kathodenkollektor"]     = (1+Zusatzverlust)*dictionary["Kathodenkollektor"]
        dictionary["Anodenbeschichtung"]    = (1+Zusatzverlust)*dictionary["Anodenbeschichtung"]
        dictionary["Kathodenbeschichtung"]  = (1+Zusatzverlust)*dictionary["Kathodenbeschichtung"]
        dictionary["Separator"]             = (1+Zusatzverlust)*dictionary["Separator"]
        dictionary["Elektrolyt"]            = (1+Zusatzverlust)*dictionary["Elektrolyt"]  
        
        return dictionary
    
    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/365
        Zeit_pro_Zelle = (self.Zellergebnisse["Wert"]['Anzahl Wiederholeinheiten']*4)/float(self.df["Wert"]["Geschwindigkeit"])+float(self.df["Wert"]["Nebenzeiten"]) #[s]
        Anz_Maschinen = math.ceil(Zellen_pro_Tag/(24*60*60/Zeit_pro_Zelle))
        dictionary["Anzahl Maschinen"] = Anz_Maschinen
        self.Anlagen = Anz_Maschinen
        
        return dictionary
    
    def mitarbeiter_anlagen(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   (self.Anlagen)*self.df["Wert"]["Personal Facharbeiter"]
        dictionary["Personalbedarf Hilfskraft"]     =   (self.Anlagen)*self.df["Wert"]["Personal Hilfskräfte"]
        
        return dictionary
    
    def energie(self,dictionary):
        dictionary["Energiebedarf"] =   (self.Anlagen)*self.df["Wert"]["Leistungsaufnahme"]*24*365
        
        return dictionary
    
    def investition(self,dictionary):
        dictionary["Investition"] = self.Anlagen*self.df["Wert"]["Investition"]
        
        return dictionary
    
    def flaechen(self,dictionary):
        dictionary["Flächenbedarf"]             =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche"]
        dictionary["Flächenbedarf Trockenraum"] =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche Trockenraum"]
 
        return dictionary

#____________________________________
#Prozessschritte für Zellen         
class zelle_prozessschritt(basis_prozessschritt):
    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/365
        Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
        Anz_Maschinen = math.ceil(Zellen_pro_Minute/float(self.df["Wert"]["Geschwindigkeit"]))
        dictionary["Anzahl Maschinen"] = Anz_Maschinen
        self.Anlagen = Anz_Maschinen
        return dictionary
    
    def mitarbeiter_anlagen(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   (self.Anlagen)*self.df["Wert"]["Personal Facharbeiter"]
        dictionary["Personalbedarf Hilfskraft"]     =   (self.Anlagen)*self.df["Wert"]["Personal Hilfskräfte"]
        
        return dictionary
    
    def energie(self,dictionary):
        dictionary["Energiebedarf"] =   (self.Anlagen)*self.df["Wert"]["Leistungsaufnahme"]*24*365
                
        return dictionary
    
    def investition(self,dictionary):
        dictionary["Investition"] = self.Anlagen*self.df["Wert"]["Investition"]
        
        return dictionary
    
    def flaechen(self,dictionary):
        dictionary["Flächenbedarf"]             =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche"]
        dictionary["Flächenbedarf Trockenraum"] =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche Trockenraum"]

        return dictionary
    
    def fixausschuss(self,dictionary):
        
        return dictionary

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

def read_zellinfo(Material, df):
    df = df.loc[df["Material"] == Material]
    return df


#____________________________________
#Prozessfunktionen
def Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    faktor_ueberkapazitaet = (1+float(df["Wert"]["Überkapazität"])/100) #[%], 1+Überkapazität/100
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    #Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    #Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]
    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]/Zellchemie["Wert"]["Feststoffgehalt Anode"]/100000
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]/Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100000

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode
    
    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} Kathode, {} Dosierer Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    float(df["Wert"]["Investition einmalig"])+\
                    (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Investition Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"]) + (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])
    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
        
    schritt_dictionary["Flächenbedarf Trockenraum"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    
    return schritt_dictionary

def Trockenbeschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    return schritt_dictionary

def Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = 3*(2+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = 3*(2+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = (Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode)*(1-float(df["Wert"]["Faktor Trockenraum"])) #[m²]
    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode*float(df["Wert"]["Faktor Trockenraum"]) #[m²]

    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")

    return schritt_dictionary

def Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def Prälithiierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary
    
def Strukturierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Intensivtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Vereinzeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Anodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
    meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektor,Materialinfos)["Wert"]["Rollenlänge"]
    
    Kathodenkollektor = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]
    meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektor,Materialinfos)["Wert"]["Rollenlänge"]
    
    Zusatzverlust_Anodenkollektor = float(df["Wert"]["Fixausschuss"])/meter_anodenkollektorfolie_pro_rolle
    Zusatzverlust_Kathodenkollektor = float(df["Wert"]["Fixausschuss"])/meter_kathodenkollektorfolie_pro_rolle
    
    Zusatzverlust = (Zusatzverlust_Anodenkollektor + Zusatzverlust_Kathodenkollektor)/2
    
    schritt_dictionary["Zelläquivalent"]        = schritt_dictionary["Zelläquivalent"]*(1+Zusatzverlust)
    schritt_dictionary["Anodenkollektor"]       = schritt_dictionary["Anodenkollektor"]*(1+Zusatzverlust_Anodenkollektor)
    schritt_dictionary["Kathodenkollektor"]     = schritt_dictionary["Kathodenkollektor"]*(1+Zusatzverlust_Kathodenkollektor)
    schritt_dictionary["Anodenbeschichtung"]    = schritt_dictionary["Anodenbeschichtung"]*(1+Zusatzverlust_Anodenkollektor)
    schritt_dictionary["Kathodenbeschichtung"]  = schritt_dictionary["Kathodenbeschichtung"]*(1+Zusatzverlust_Kathodenkollektor)
    schritt_dictionary["Separator"]             = schritt_dictionary["Separator"]*(1+Zusatzverlust)
    schritt_dictionary["Elektrolyt"]            = schritt_dictionary["Elektrolyt"]*(1+Zusatzverlust)
        
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
  
    return schritt_dictionary

def Laminieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Stapeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    
    return schritt_dictionary

def Wickeln_Z_Falten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def Wickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["Variabler Ausschuss"])/100)
    
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
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    Facharbeiter = Anzahl_Anlagen*df["Wert"]["Personal Facharbeiter"]
    Hilfskraft = Anzahl_Anlagen*float(df["Wert"]["Personal Hilfskräfte"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Anzahl Maschinen": Anzahl_Anlagen,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "Personlabedarf Facharbeiter":Facharbeiter,
        "Personalbedarf Hilfskraft":Hilfskraft,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Separator"
                }                    
    materialien_null_setzen(liste,schritt_dictionary)    

    return schritt_dictionary

def Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary


def Assemblieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary


def Pouchbeutel___Gehäuse_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary


def Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/365
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Durchsatz_pro_Minute = 60*float(df["Wert"]["Parallelbefüllungen"])/float(df["Wert"]["Befülldauer je Zelle"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    
    return schritt_dictionary


def Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary
    

def Formieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
  
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Module = math.ceil(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz"]))
    Bediengeräte = math.ceil(float(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz Bediengerät"])))
    
    schritt_dictionary["Investition"]=Module*float(df["Wert"]["Investition Modul"])+Bediengeräte*float(df["Wert"]["Investition Bediengerät"])
    
    schritt_dictionary["Flächenbedarf"]=Module*float(df["Wert"]["Anlagengrundfläche"])/10
    schritt_dictionary["Flächenbedarf Trockenraum"]=Module*float(df["Wert"]["Anlagengrundfläche Trockenraum"])/10
    
    schritt_dictionary["Anzahl Maschinen"]= "{} Module, {} Bediengeräte".format(Module,Bediengeräte)
    
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
    
    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 #[kWh]
    
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

    
def Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    
    Bediengeräte = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Tagesdurchsatz Bediengerät"]))
    Module = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Zellen/Modul"]))
    Tuerme = math.ceil(Module/float(df["Wert"]["Module/Turm"]))
    process.Anlagen = Tuerme
    
    schritt_dictionary["Anzahl Maschinen"] = "{} Module, {} Türme, {} Bediengeräte".format(Module,Tuerme,Bediengeräte)
    schritt_dictionary["Investition"] = Bediengeräte*float(df["Wert"]["Investition Bediengerät"])+Module*float(df["Wert"]["Investition Modul"])
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)  
    schritt_dictionary = process.neue_materialien(schritt_dictionary)   
    
    return schritt_dictionary


def Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

#_____________________________________________________________________________
#neue Paper Schritte

def Zellwickel_Einbau(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Cap_verschließen_und_kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Precharge_und_Entgasen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Flachwickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["Variabler Ausschuss"])/100)
    
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
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    Facharbeiter = Anzahl_Anlagen*df["Wert"]["Personal Facharbeiter"]
    Hilfskraft = Anzahl_Anlagen*float(df["Wert"]["Personal Hilfskräfte"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Anzahl Maschinen": Anzahl_Anlagen,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "Personlabedarf Facharbeiter":Facharbeiter,
        "Personalbedarf Hilfskraft":Hilfskraft,
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
def MultiEx_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
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

    Anlagen_Anode = math.ceil(Liter_Anode_pro_Tag/24/df["Wert"]["Geschwindigkeit"])
    Anlagen_Kathode = math.ceil(Liter_Kathode_pro_Tag/24/df["Wert"]["Geschwindigkeit"])
    
    Anz_Maschinen=Anlagen_Anode+Anlagen_Kathode

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    
    Energiebedarf = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
   
    Facharbeiter = Anzahl_Anlagen*df["Wert"]["Personal Facharbeiter"]
    Hilfskraft = Anzahl_Anlagen*float(df["Wert"]["Personal Hilfskräfte"])
        
    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Anzahl Maschinen": Anz_Maschinen,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "Personlabedarf Facharbeiter":Facharbeiter,
        "Personalbedarf Hilfskraft":Hilfskraft,
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


def Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def MiKal_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    faktor_ueberkapazitaet = (1+float(df["Wert"]["Überkapazität"])/100) #[%], 1+Überkapazität/100
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode
    
    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} Kathode, {} Dosierer Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    float(df["Wert"]["Investition einmalig"])+\
                    (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Investition Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"]) + (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])
    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
        
    schritt_dictionary["Flächenbedarf Trockenraum"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    return schritt_dictionary

def OptiEx(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    faktor_ueberkapazitaet = (1+float(df["Wert"]["Überkapazität"])/100) #[%], 1+Überkapazität/100
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode
    
    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} Kathode, {} Dosierer Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    float(df["Wert"]["Investition einmalig"])+\
                    (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Investition Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"]) + (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])
    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
        
    schritt_dictionary["Flächenbedarf Trockenraum"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    return schritt_dictionary

def ÖkoTroP_Bürstenauftrag(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def ÖkoTroP_Elektrostatisch(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def HighStructures_Extrusion(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def HighStructures_Laser(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Epic(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def RollBatt(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def PräLi_Li_Salz(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def PräLi_PVD(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def PräLi_Opferanode(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def HoLiB_Vereinzeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def E_Qual(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def ProfiStruk_Strukturierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def HoLiB_Stapeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    return schritt_dictionary

def Cell_Fill_Separatormodifikation(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary

def Cell_Fill_Befüllen_und_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/365
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Durchsatz_pro_Minute = 60*float(df["Wert"]["Parallelbefüllungen"])/float(df["Wert"]["Befülldauer je Zelle"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    return schritt_dictionary

def FormEl(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    return schritt_dictionary



#Prozesse fürs Paper

#PHEV 2 Produktion

def PHEV2_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    faktor_ueberkapazitaet = (1+float(df["Wert"]["Überkapazität"])/100) #[%], 1+Überkapazität/100
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode
    
    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} Kathode, {} Dosierer Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    float(df["Wert"]["Investition einmalig"])+\
                    (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Investition Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"]) + (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])
    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
        
    schritt_dictionary["Flächenbedarf Trockenraum"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    
    return schritt_dictionary

def PHEV2_Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    return schritt_dictionary

def PHEV2_Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = 3*(2+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = 3*(2+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = (Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode)*(1-float(df["Wert"]["Faktor Trockenraum"])) #[m²]
    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode*float(df["Wert"]["Faktor Trockenraum"]) #[m²]

    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")

    return schritt_dictionary

def PHEV2_Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Flachwickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["Variabler Ausschuss"])/100)
    
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
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    Facharbeiter = Anzahl_Anlagen*df["Wert"]["Personal Facharbeiter"]
    Hilfskraft = Anzahl_Anlagen*float(df["Wert"]["Personal Hilfskräfte"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Anzahl Maschinen": Anzahl_Anlagen,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "Personlabedarf Facharbeiter":Facharbeiter,
        "Personalbedarf Hilfskraft":Hilfskraft,
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

def PHEV2_Cap_verschließen_und_kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/365
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Durchsatz_pro_Minute = 60*float(df["Wert"]["Parallelbefüllungen"])/float(df["Wert"]["Befülldauer je Zelle"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    
    return schritt_dictionary

def PHEV2_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Formieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
  
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Module = math.ceil(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz"]))
    Bediengeräte = math.ceil(float(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz Bediengerät"])))
    
    schritt_dictionary["Investition"]=Module*float(df["Wert"]["Investition Modul"])+Bediengeräte*float(df["Wert"]["Investition Bediengerät"])
    
    schritt_dictionary["Flächenbedarf"]=Module*float(df["Wert"]["Anlagengrundfläche"])/10
    schritt_dictionary["Flächenbedarf Trockenraum"]=Module*float(df["Wert"]["Anlagengrundfläche Trockenraum"])/10
    
    schritt_dictionary["Anzahl Maschinen"]= "{} Module, {} Bediengeräte".format(Module,Bediengeräte)
    
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
    
    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 #[kWh]
    
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary
    
def PHEV2_Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    
    Bediengeräte = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Tagesdurchsatz Bediengerät"]))
    Module = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Zellen/Modul"]))
    Tuerme = math.ceil(Module/float(df["Wert"]["Module/Turm"]))
    process.Anlagen = Tuerme
    
    schritt_dictionary["Anzahl Maschinen"] = "{} Module, {} Türme, {} Bediengeräte".format(Module,Tuerme,Bediengeräte)
    schritt_dictionary["Investition"] = Bediengeräte*float(df["Wert"]["Investition Bediengerät"])+Module*float(df["Wert"]["Investition Modul"])
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)  
    schritt_dictionary = process.neue_materialien(schritt_dictionary)   
    
    return schritt_dictionary

def PHEV2_Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def PHEV2_Verpackung_und_Versand(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary


#Tesla 4680 Produktion

def Tesla_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    faktor_ueberkapazitaet = (1+float(df["Wert"]["Überkapazität"])/100) #[%], 1+Überkapazität/100
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(1-Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode
    
    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} Kathode, {} Dosierer Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    float(df["Wert"]["Investition einmalig"])+\
                    (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Investition Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"]) + (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])
    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
        
    schritt_dictionary["Flächenbedarf Trockenraum"] = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    
    return schritt_dictionary

def Tesla_Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    return schritt_dictionary

def Tesla_Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = 3*(2+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = 3*(2+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = (Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode)*(1-float(df["Wert"]["Faktor Trockenraum"])) #[m²]
    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode+Anlagengrundfläche_Kathode*float(df["Wert"]["Faktor Trockenraum"]) #[m²]

    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")

    return schritt_dictionary

def Tesla_Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.fixausschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Wickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    
    Verlust = (1+float(df["Wert"]["Variabler Ausschuss"])/100)
    
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
    
    Investition = Anzahl_Anlagen*float(df["Wert"]["Investition"])
    Flächenbedarf = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche"])
    Flächenbedarf_Trockenraum = Anzahl_Anlagen*float(df["Wert"]["Anlagengrundfläche Trockenraum"])
    Energiebedarf = Anzahl_Anlagen*float(df["Wert"]["Leistungsaufnahme"])*24*arbeitstage_pro_jahr
    Facharbeiter = Anzahl_Anlagen*df["Wert"]["Personal Facharbeiter"]
    Hilfskraft = Anzahl_Anlagen*float(df["Wert"]["Personal Hilfskräfte"])

    liste = neue_materialien_zu_liste(schritt_dictionary["Neue Materialien"])    
    schritt_dictionary={
        "Zelläquivalent":Zelläquivalent,
        "Investition":Investition,
        "Anzahl Maschinen": Anzahl_Anlagen,
        "Flächenbedarf":Flächenbedarf,
        "Flächenbedarf Trockenraum":Flächenbedarf_Trockenraum,
        "Personlabedarf Facharbeiter":Facharbeiter,
        "Personalbedarf Hilfskraft":Hilfskraft,
        "Energiebedarf":Energiebedarf,
        "Anodenkollektor":Anodenkollektor,
        "Kathodenkollektor":Kathodenkollektor,
        "Anodenbeschichtung":Anodenbeschichtung,
        "Kathodenbeschichtung":Kathodenbeschichtung,
        "Separator":Separator,
        "Elektrolyt":Elektrolyt,
        "Neue Materialien":"Separator"
                }                    
    materialien_null_setzen(liste,schritt_dictionary)    

    return schritt_dictionary

def Tesla_Cap_verschließen_und_kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/365
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Durchsatz_pro_Minute = 60*float(df["Wert"]["Parallelbefüllungen"])/float(df["Wert"]["Befülldauer je Zelle"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    
    return schritt_dictionary

def Tesla_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Formieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
  
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Module = math.ceil(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz"]))
    Bediengeräte = math.ceil(float(Zellen_pro_Tag/float(df["Wert"]["Tagesdurchsatz Bediengerät"])))
    
    schritt_dictionary["Investition"]=Module*float(df["Wert"]["Investition Modul"])+Bediengeräte*float(df["Wert"]["Investition Bediengerät"])
    
    schritt_dictionary["Flächenbedarf"]=Module*float(df["Wert"]["Anlagengrundfläche"])/10
    schritt_dictionary["Flächenbedarf Trockenraum"]=Module*float(df["Wert"]["Anlagengrundfläche Trockenraum"])/10
    
    schritt_dictionary["Anzahl Maschinen"]= "{} Module, {} Bediengeräte".format(Module,Bediengeräte)
    
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
    
    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 #[kWh]
    
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary
    
def Tesla_Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    
    Bediengeräte = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Tagesdurchsatz Bediengerät"]))
    Module = math.ceil(Zellen_pro_Tag*float(df["Wert"]["Reifelagerdauer"])/float(df["Wert"]["Zellen/Modul"]))
    Tuerme = math.ceil(Module/float(df["Wert"]["Module/Turm"]))
    process.Anlagen = Tuerme
    
    schritt_dictionary["Anzahl Maschinen"] = "{} Module, {} Türme, {} Bediengeräte".format(Module,Tuerme,Bediengeräte)
    schritt_dictionary["Investition"] = Bediengeräte*float(df["Wert"]["Investition Bediengerät"])+Module*float(df["Wert"]["Investition Modul"])
    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_schicht(schritt_dictionary)  
    schritt_dictionary = process.neue_materialien(schritt_dictionary)   
    
    return schritt_dictionary

def Tesla_Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Tesla_Verpackung_und_Versand(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary
