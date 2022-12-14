# -*- coding: utf-8 -*-iebs
"""
Created on Wed Feb 24 10:08:39 2021

@author: bendzuck
"""

import math

#____________________________________
#HARDCODED WERTE, BITTE ANPASSEN
arbeitstage_pro_jahr=360

#____________________________________
#Klassen

class basis_prozessschritt:
    def __init__(self,df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung):
        self.df = df
        self.Zellergebnisse = Zellergebnisse
        self.Zellchemie = Zellchemie
        self.Materialinfos = Materialinfos

            
    def variabler_aussschuss(self,dictionary):
        dictionary["Zelläquivalent"]        = dictionary["Zelläquivalent"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[-]
        dictionary["Anodenkollektor"]       = dictionary["Anodenkollektor"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Kathodenkollektor"]     = dictionary["Kathodenkollektor"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Anodenbeschichtung"]    = dictionary["Anodenbeschichtung"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[kg]
        dictionary["Kathodenbeschichtung"]  = dictionary["Kathodenbeschichtung"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[kg]
        dictionary["Separator"]             = dictionary["Separator"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Hülle"]                 = dictionary["Hülle"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        dictionary["Elektrolyt"]            = dictionary["Elektrolyt"]/(1-self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        
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
                                        self.Anlagen_Kathode*self.df["Wert"]["Leistungsaufnahme Kathode"])*24*arbeitstage_pro_jahr #[kWh]
        return dictionary
    
    def investition(self,dictionary):
        dictionary["Investition"] = self.Anlagen_Anode*self.df["Wert"]["Investition Anode"] + self.Anlagen_Kathode*self.df["Wert"]["Investition Kathode"] #[€]
        return dictionary

    def ueberkapazitaet(self, dictionary):
        faktor_ueberkapazitaet = 1 + self.df["Wert"]["Überkapazität"]/100
        self.Anlagen_Anode = math.ceil(self.Anlagen_Anode*faktor_ueberkapazitaet)
        self.Anlagen_Kathode = math.ceil(self.Anlagen_Kathode*faktor_ueberkapazitaet)
        return dictionary
    
    def neue_materialien(self,dictionary,neue_materialien=""):
        neue_materialen_liste = dictionary["Neue Materialien"].split(';')
        if neue_materialen_liste != [""]:
            for material in neue_materialen_liste:
                dictionary[material]=0
                dictionary[material+" Rückgewinnung"]=0
            dictionary["Neue Materialien"] = neue_materialien
            return dictionary
        else:
            dictionary["Neue Materialien"] = neue_materialien
            return dictionary
#____________________________________
#Prozessschritte für Suspensionen
class suspension_prozessschritt(basis_prozessschritt):
    def rueckgewinnung(self,dictionary,rueckgewinnung):
        dictionary["Anodenkollektor Rückgewinnung"]       = dictionary["Anodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Kathodenkollektor Rückgewinnung"]     = dictionary["Kathodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Anodenbeschichtung Rückgewinnung"]    = dictionary["Anodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Slurry-Rohmaterialien Anode"]/100 #[kg]
        dictionary["Kathodenbeschichtung Rückgewinnung"]  = dictionary["Kathodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Slurry-Rohmaterialien Kathode"]/100 #[kg]
        dictionary["Separator Rückgewinnung"]             = dictionary["Separator"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Hülle Rückgewinnung"]                 = dictionary["Hülle"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        dictionary["Elektrolyt Rückgewinnung"]            = dictionary["Elektrolyt"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        
        return dictionary

    def fixausschuss(self,dictionary,rueckgewinnung):

        return dictionary

#____________________________________
#Prozessschritte für Rolle-zu-Rolle Prozesse
class coil_prozessschritt(basis_prozessschritt):
    def rueckgewinnung(self,dictionary,rueckgewinnung):
        dictionary["Anodenkollektor Rückgewinnung"]       = dictionary["Anodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Anode"]/100 #[m]
        dictionary["Kathodenkollektor Rückgewinnung"]     = dictionary["Kathodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Kathode"]/100 #[m]
        dictionary["Anodenbeschichtung Rückgewinnung"]    = dictionary["Anodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Anode"]/100 #[kg]
        dictionary["Kathodenbeschichtung Rückgewinnung"]  = dictionary["Kathodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Kathode"]/100 #[kg]
        dictionary["Separator Rückgewinnung"]             = dictionary["Separator"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Hülle Rückgewinnung"]                 = dictionary["Hülle"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        dictionary["Elektrolyt Rückgewinnung"]            = dictionary["Elektrolyt"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        
        return dictionary

    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

        Meter_Anode_pro_Tag = Zellen_pro_Tag*self.Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/self.Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
        Meter_Kathode_pro_Tag = Zellen_pro_Tag*self.Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/self.Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

        Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
        Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)
        
        Anodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
        meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        Kathodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]
        meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        
        Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/float(self.df["Wert"]["Geschwindigkeit Anode"]) #[min]
        Verlust_durch_Nebenzeit_Anode = self.df["Wert"]["Nebenzeit Anode"]/Zeit_pro_Coil_Anode #[%]
        
        Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/float(self.df["Wert"]["Geschwindigkeit Kathode"])
        Verlust_durch_Nebenzeit_Kathode = float(self.df["Wert"]["Nebenzeit Kathode"])/Zeit_pro_Coil_Kathode #[%]
        
        Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/float(self.df["Wert"]["Geschwindigkeit Anode"])*(1+Verlust_durch_Nebenzeit_Anode))
        Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/float(self.df["Wert"]["Geschwindigkeit Kathode"])*(1+Verlust_durch_Nebenzeit_Kathode))

        Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

        self.Anlagen_Anode = Anlagen_Anode
        self.Anlagen_Kathode = Anlagen_Kathode

        dictionary["Anzahl Maschinen"] = Anz_Maschinen

        return dictionary

    def flaechen_getrennt(self,dictionary):
        dictionary["Flächenbedarf"]             =   self.Anlagen_Anode*self.df["Wert"]["Anlagengrundfläche Anode"]+\
                                                    self.Anlagen_Kathode*self.df["Wert"]["Anlagengrundfläche Kathode"] #[m²]

        dictionary["Flächenbedarf Trockenraum"] =   self.Anlagen_Anode*self.df["Wert"]["Anlagengrundfläche Trockenraum Anode"]+\
                                                    self.Anlagen_Kathode*self.df["Wert"]["Anlagengrundfläche Trockenraum Kathode"] #[m²]
        return dictionary

    #Fixausschuss pro Coil
    def fixausschuss(self,dictionary,rueckgewinnung):       
        Anodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
        meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        Kathodenkollektorfolie = self.Zellchemie.loc[self.Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]
        meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,self.Materialinfos)["Wert"]["Rollenlänge"]
        
        Zusatzverlust_Anode = self.df["Wert"]["Fixausschuss"]/meter_anodenkollektorfolie_pro_rolle
        Zusatzverlust_Kathode = self.df["Wert"]["Fixausschuss"]/meter_kathodenkollektorfolie_pro_rolle
        
        Zusatzverlust = (Zusatzverlust_Anode+Zusatzverlust_Kathode)/2
        
        dictionary["Zelläquivalent"]        = dictionary["Zelläquivalent"]/(1-Zusatzverlust)
        dictionary["Anodenkollektor"]       = dictionary["Anodenkollektor"]/(1-Zusatzverlust)
        dictionary["Kathodenkollektor"]     = dictionary["Kathodenkollektor"]/(1-Zusatzverlust)
        dictionary["Anodenbeschichtung"]    = dictionary["Anodenbeschichtung"]/(1-Zusatzverlust)
        dictionary["Kathodenbeschichtung"]  = dictionary["Kathodenbeschichtung"]/(1-Zusatzverlust)
        dictionary["Separator"]             = dictionary["Separator"]/(1-Zusatzverlust)
        dictionary["Hülle"]                 = dictionary["Hülle"]/(1-Zusatzverlust)
        dictionary["Elektrolyt"]            = dictionary["Elektrolyt"]/(1-Zusatzverlust)

        dictionary["Anodenkollektor Rückgewinnung"] = dictionary["Anodenkollektor Rückgewinnung"]+dictionary["Anodenkollektor"]*Zusatzverlust_Anode*rueckgewinnung["Wert"]["Anodenkollektor"]/100
        dictionary["Kathodenkollektor Rückgewinnung"] = dictionary["Kathodenkollektor Rückgewinnung"]+dictionary["Kathodenkollektor"]*Zusatzverlust_Kathode*rueckgewinnung["Wert"]["Kathodenkollektor"]/100
        
        return dictionary
    
#____________________________________
#Prozessschritte für Elektrodenblätter     
class sheet_prozessschritt(basis_prozessschritt):
    def rueckgewinnung(self,dictionary,rueckgewinnung):
        dictionary["Anodenkollektor Rückgewinnung"]       = dictionary["Anodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Anode"]/100 #[m]
        dictionary["Kathodenkollektor Rückgewinnung"]     = dictionary["Kathodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Kathode"]/100 #[m]
        dictionary["Anodenbeschichtung Rückgewinnung"]    = dictionary["Anodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Anode"]/100 #[kg]
        dictionary["Kathodenbeschichtung Rückgewinnung"]  = dictionary["Kathodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Kathode"]/100 #[kg]
        dictionary["Separator Rückgewinnung"]             = dictionary["Separator"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[m]
        dictionary["Hülle Rückgewinnung"]                 = dictionary["Hülle"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        dictionary["Elektrolyt Rückgewinnung"]            = dictionary["Elektrolyt"]*(self.df["Wert"]["Variabler Ausschuss"]/100) #[l]
        
        return dictionary

    def fixausschuss(self,dictionary,rueckgewinnung):
        WHE_pro_tag = dictionary["Zelläquivalent"]/arbeitstage_pro_jahr*(self.Zellergebnisse["Wert"]['Anzahl Wiederholeinheiten'])
        sheet_pro_tag = WHE_pro_tag*2
        Fixausschuss = self.df["Wert"]["Fixausschuss"]#Stk./d
        
        Zusatzverlust = Fixausschuss/sheet_pro_tag      
        
        dictionary["Zelläquivalent"]        = dictionary["Zelläquivalent"]/(1-Zusatzverlust)
        dictionary["Anodenkollektor"]       = dictionary["Anodenkollektor"]/(1-Zusatzverlust)
        dictionary["Kathodenkollektor"]     = dictionary["Kathodenkollektor"]/(1-Zusatzverlust)
        dictionary["Anodenbeschichtung"]    = dictionary["Anodenbeschichtung"]/(1-Zusatzverlust)
        dictionary["Kathodenbeschichtung"]  = dictionary["Kathodenbeschichtung"]/(1-Zusatzverlust)
        dictionary["Separator"]             = dictionary["Separator"]/(1-Zusatzverlust)
        dictionary["Elektrolyt"]            = dictionary["Elektrolyt"]/(1-Zusatzverlust)

        dictionary["Anodenkollektor Rückgewinnung"] = dictionary["Anodenkollektor Rückgewinnung"]+dictionary["Anodenkollektor"]*Zusatzverlust*rueckgewinnung["Wert"]["Anodenkollektor"]/100
        dictionary["Kathodenkollektor Rückgewinnung"] = dictionary["Kathodenkollektor Rückgewinnung"]+dictionary["Kathodenkollektor"]*Zusatzverlust*rueckgewinnung["Wert"]["Kathodenkollektor"]/100
        dictionary["Anodenbeschichtung Rückgewinnung"] = dictionary["Anodenbeschichtung Rückgewinnung"]+dictionary["Anodenbeschichtung"]*Zusatzverlust*rueckgewinnung["Wert"]["Anodenbeschichtung"]/100
        dictionary["Kathodenbeschichtung Rückgewinnung"] = dictionary["Kathodenbeschichtung Rückgewinnung"]+dictionary["Kathodenbeschichtung"]*Zusatzverlust*rueckgewinnung["Wert"]["Kathodenbeschichtung"]/100

        return dictionary
    
    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
        Zeit_pro_Zelle = (self.Zellergebnisse["Wert"]['Anzahl Wiederholeinheiten']*4)/float(self.df["Wert"]["Geschwindigkeit"])+float(self.df["Wert"]["Nebenzeiten"]) #[s]
        Anz_Maschinen = math.ceil(Zellen_pro_Tag/(24*60*60/Zeit_pro_Zelle))
        dictionary["Anzahl Maschinen"] = Anz_Maschinen
        self.Anlagen = Anz_Maschinen
        
        return dictionary

    def ueberkapazitaet(self, dictionary):
        faktor_ueberkapazitaet = 1 + self.df["Wert"]["Überkapazität"]/100
        self.Anlagen = math.ceil(self.Anlagen*faktor_ueberkapazitaet)
        return dictionary
    
    def mitarbeiter_anlagen(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   (self.Anlagen)*self.df["Wert"]["Personal Facharbeiter"]
        dictionary["Personalbedarf Hilfskraft"]     =   (self.Anlagen)*self.df["Wert"]["Personal Hilfskräfte"]
        
        return dictionary
    
    def energie(self,dictionary):
        dictionary["Energiebedarf"] =   (self.Anlagen)*self.df["Wert"]["Leistungsaufnahme"]*24*arbeitstage_pro_jahr
        
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
    def rueckgewinnung(self,dictionary,rueckgewinnung):
        dictionary["Anodenkollektor Rückgewinnung"]       = dictionary["Anodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[m]
        dictionary["Kathodenkollektor Rückgewinnung"]     = dictionary["Kathodenkollektor"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[m]
        dictionary["Anodenbeschichtung Rückgewinnung"]    = dictionary["Anodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[kg]
        dictionary["Kathodenbeschichtung Rückgewinnung"]  = dictionary["Kathodenbeschichtung"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[kg]
        dictionary["Separator Rückgewinnung"]             = dictionary["Separator"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[m]
        dictionary["Hülle Rückgewinnung"]                 = dictionary["Hülle"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[l]
        dictionary["Elektrolyt Rückgewinnung"]            = dictionary["Elektrolyt"]*(self.df["Wert"]["Variabler Ausschuss"]/100)*rueckgewinnung["Wert"]["Befüllte Zelle"]/100 #[l]
        
        return dictionary

    def anlagen(self,dictionary):
        Zellen_pro_Tag = dictionary["Zelläquivalent"]/arbeitstage_pro_jahr+self.df["Wert"]["Fixausschuss"]
        Zellen_pro_Minute = Zellen_pro_Tag/(24*60)
        Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+self.df["Wert"]["Nebenzeit"]) 
        Anz_Maschinen = math.ceil(Zellen_pro_Minute/float(self.df["Wert"]["Geschwindigkeit"]))
        dictionary["Anzahl Maschinen"] = Anz_Maschinen
        self.Anlagen = Anz_Maschinen
        return dictionary
    
    def mitarbeiter_anlagen(self,dictionary):
        dictionary["Personlabedarf Facharbeiter"]   =   (self.Anlagen)*self.df["Wert"]["Personal Facharbeiter"]
        dictionary["Personalbedarf Hilfskraft"]     =   (self.Anlagen)*self.df["Wert"]["Personal Hilfskräfte"]
        
        return dictionary
    
    def energie(self,dictionary):
        dictionary["Energiebedarf"] =   (self.Anlagen)*self.df["Wert"]["Leistungsaufnahme"]*24*arbeitstage_pro_jahr
                
        return dictionary

    def ueberkapazitaet(self, dictionary):
        faktor_ueberkapazitaet = 1 + self.df["Wert"]["Überkapazität"]/100
        self.Anlagen = math.ceil(self.Anlagen*faktor_ueberkapazitaet)
        return dictionary
    
    def investition(self,dictionary):
        dictionary["Investition"] = self.Anlagen*self.df["Wert"]["Investition"]
        
        return dictionary
    
    def flaechen(self,dictionary):
        dictionary["Flächenbedarf"]             =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche"]
        dictionary["Flächenbedarf Trockenraum"] =   (self.Anlagen)*self.df["Wert"]["Anlagengrundfläche Trockenraum"]

        return dictionary
    
    def fixausschuss(self,dictionary,rueckgewinnung):
        
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
def Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
     
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = math.ceil(process.Anlagen_Anode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))
    process.Anlagen_Kathode = math.ceil(process.Anlagen_Kathode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Trockenbeschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    return schritt_dictionary

def Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary


def Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = Anlagengrundfläche_Anode*(1-float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(1-float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]

    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode*(float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]
    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen_Anode+process.Anlagen_Kathode
    schritt_dictionary = process.investition(schritt_dictionary)
    
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    return schritt_dictionary

def Prälithiierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

    
def Strukturierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0

    print("Längssschneiden")
    print(schritt_dictionary)
    return schritt_dictionary

def Intensivtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    #schritt_dictionary = process.anlagen(schritt_dictionary)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Anodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
    Kathodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
    Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)

    Geschwindigkeit_Anode = float(df["Wert"]["Geschwindigkeit Anode"])/(read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    Geschwindigkeit_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])/(read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    
    meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    
    Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/Geschwindigkeit_Anode #[min]
    Verlust_durch_Nebenzeit_Anode = df["Wert"]["Nebenzeit Anode"]/Zeit_pro_Coil_Anode #[%]
    
    Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/Geschwindigkeit_Kathode
    Verlust_durch_Nebenzeit_Kathode = float(df["Wert"]["Nebenzeit Kathode"])/Zeit_pro_Coil_Kathode #[%]
    
    Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/Geschwindigkeit_Anode*(1+Verlust_durch_Nebenzeit_Anode))
    Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/Geschwindigkeit_Kathode*(1+Verlust_durch_Nebenzeit_Kathode))

    Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Anzahl Maschinen"] = Anz_Maschinen

    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Vereinzeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    
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
    schritt_dictionary["Flächenbedarf Labor"] = 0

    print("Vereinzeln")
    print(schritt_dictionary)
  
    return schritt_dictionary

def Laminieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Stapeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    
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
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Wickeln_Z_Falten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    return schritt_dictionary

def Wickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)   
    
    laenge_anodensheet = Zellergebnisse["Wert"]["Sheets/ Meter Anode"]*Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"] #[m/Zelle]
    Zellen_pro_Minute = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr/24/60 #[Zellen/min]

    #Meter_Anode_pro_minute = laenge_anodensheet * Zellen_pro_Minute #[m/min]
    Kapazitaet_Anlage = df["Wert"]["Geschwindigkeit"]/laenge_anodensheet #[Zellen/min]
    Zeit_pro_Zelle = 1/Kapazitaet_Anlage
    Zeit_pro_Zelle_mit_nebenzeit = Zeit_pro_Zelle+df["Wert"]["Nebenzeit"]
    Kapazitaet_Anlage_mit_nebenzeit = 1/Zeit_pro_Zelle_mit_nebenzeit

    process.Anlagen = math.ceil(Zellen_pro_Minute/Kapazitaet_Anlage_mit_nebenzeit)

    schritt_dictionary["Personlabedarf Facharbeiter"] = process.Anlagen*df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = process.Anlagen*df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = process.Anlagen*df["Wert"]["Leistungsaufnahme"]*arbeitstage_pro_jahr*24

    process.Anlagen = math.ceil(process.Anlagen * (1+df["Wert"]["Überkapazität"]/100))

    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen
    schritt_dictionary["Flächenbedarf"] = process.Anlagen*df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Trockenraum"]

    schritt_dictionary["Investition"] = process.Anlagen*df["Wert"]["Investition"]

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Assemblieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Pouchbeutel___Gehäuse_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary
    


def Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = float(df["Wert"]["Parallelbefüllungen"])*float(df["Wert"]["Geschwindigkeit"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary
    

def Formieren_und_Entgasen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Formierdauer"])*60/float(df["Wert"]["Anzahl Zellen/Formierturm"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    rueckgewinnungsfaktor = df["Wert"]["Rückgewinnungsfaktor"]

    Q_Z=float(Zellergebnisse["Wert"]["Ladung"]) #Speicherkapazität der Batteriezelle [Ah]
    U_OCV=float(Zellergebnisse["Wert"]["Nennspannung"]) #Klemmspannung [Volt]
    Eta_C1=float(df["Wert"]["Eta C1"]) #Coulombscher Wirkungsgrad des ersten Ladezyklus [-]
    Eta_Z=float(df["Wert"]["Eta Z"]) #Wirkungsgrad der Zelle [-]
    
    E_L1=Q_Z*U_OCV/(Eta_C1*Eta_Z) #Energiebedarf des 1. Ladevorgangs [Wh]
    E_E1=Q_Z*U_OCV #Energiebedarf des 1. Entladevorgangs [Wh]
    E_L2=Q_Z*U_OCV/Eta_Z #Energiebedarf des 2. Ladevorgangs [Wh]
    E_E2=Q_Z*U_OCV #Energiebedarf des 2. Entladevorgangs [Wh]
    E_L50=0.5*Q_Z*U_OCV/Eta_Z #Energiebedarf des letzten Ladevorgangs auf 50% SOC [Wh]
    E_FormZ=E_L1+E_L2+E_L50-(E_E1+E_E2)*rueckgewinnungsfaktor/100 #Energiebedarf Formierung einer Zelle [Wh]

    kanaele_3_monats_test = df["Wert"]["Stichproben pro Schicht 3 Monatstest"] *3*3*30 #3 Schichten pro Tag (HARDCODED) * 3 Monate * 30 Tage
    kanaele_6_monats_test = df["Wert"]["Stichproben pro Schicht 6 Monatstest"] *3*6*30 #3 Schichten pro Tag (HARDCODED) * 6 Monate * 30 Tage
    #kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"] * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"]*3 * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    lebensdauer_kanaele_gesamt = kanaele_3_monats_test + kanaele_6_monats_test + kanaele_80_cutoff_test
    anzahl_test_anlagen = math.ceil(lebensdauer_kanaele_gesamt/ df["Wert"]["Anzahl Zellen/Formierturm"])

    energiebedarf_lebensdauertest = lebensdauer_kanaele_gesamt * Q_Z * U_OCV * df["Wert"]["C-Rate Lebensdauertest"] * 0.5 * (1-rueckgewinnungsfaktor/100)*365*24 #[Wh]
    schritt_dictionary["Anzahl Maschinen"] = "{} Anlagen, {} Testanlagen".format(process.Anlagen,anzahl_test_anlagen)
    
    process.Anlagen = process.Anlagen + anzahl_test_anlagen

    

    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 + energiebedarf_lebensdauertest/1000 #[kWh]
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

    
def Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Reifelagerdauer"])*24*60/float(df["Wert"]["Anzahl Zellen/Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

#_____________________________________________________________________________
#neue Paper Schritte

def Zellwickel_Einbau(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Hülle")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Cap_verschließen_und_kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    #schritt_dictionary = process.anlagen(schritt_dictionary)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Anodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
    Kathodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
    Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)

    Geschwindigkeit_Anode = float(df["Wert"]["Geschwindigkeit Anode"])/(read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    Geschwindigkeit_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])/(read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    
    meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    
    Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/Geschwindigkeit_Anode #[min]
    Verlust_durch_Nebenzeit_Anode = df["Wert"]["Nebenzeit Anode"]/Zeit_pro_Coil_Anode #[%]
    
    Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/Geschwindigkeit_Kathode
    Verlust_durch_Nebenzeit_Kathode = float(df["Wert"]["Nebenzeit Kathode"])/Zeit_pro_Coil_Kathode #[%]
    
    Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/Geschwindigkeit_Anode*(1+Verlust_durch_Nebenzeit_Anode))
    Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/Geschwindigkeit_Kathode*(1+Verlust_durch_Nebenzeit_Kathode))

    Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Anzahl Maschinen"] = Anz_Maschinen

    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Precharge_und_Entgasen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    
    return schritt_dictionary

def Flachwickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)   
    
    laenge_anodensheet = Zellergebnisse["Wert"]["Sheets/ Meter Anode"]*Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"] #[m/Zelle]
    Zellen_pro_Minute = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr/24/60 #[Zellen/min]

    #Meter_Anode_pro_minute = laenge_anodensheet * Zellen_pro_Minute #[m/min]
    Kapazitaet_Anlage = df["Wert"]["Geschwindigkeit"]/laenge_anodensheet #[Zellen/min]
    Zeit_pro_Zelle = 1/Kapazitaet_Anlage
    Zeit_pro_Zelle_mit_nebenzeit = Zeit_pro_Zelle+df["Wert"]["Nebenzeit"]
    Kapazitaet_Anlage_mit_nebenzeit = 1/Zeit_pro_Zelle_mit_nebenzeit

    process.Anlagen = math.ceil(Zellen_pro_Minute/Kapazitaet_Anlage_mit_nebenzeit)

    schritt_dictionary["Personlabedarf Facharbeiter"] = process.Anlagen*df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = process.Anlagen*df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = process.Anlagen*df["Wert"]["Leistungsaufnahme"]*arbeitstage_pro_jahr*24

    process.Anlagen = math.ceil(process.Anlagen * (1+df["Wert"]["Überkapazität"]/100))

    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen
    schritt_dictionary["Flächenbedarf"] = process.Anlagen*df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Trockenraum"]

    schritt_dictionary["Investition"] = process.Anlagen*df["Wert"]["Investition"]

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary


#_____________________________________________________________________________
#neue ProZell Schritte
def MultiEx_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
     
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = math.ceil(process.Anlagen_Anode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))
    process.Anlagen_Kathode = math.ceil(process.Anlagen_Kathode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Benetzungsdauer"])*60/float(df["Wert"]["Zellen pro Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary
    
def Verpackung_und_Versand(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    schritt_dictionary["Anzahl Maschinen"] = 0
    schritt_dictionary["Flächenbedarf"] = df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = df["Wert"]["Anlagengrundfläche Trockenraum"]
    schritt_dictionary["Flächenbedarf Labor"] = df["Wert"]["Anlagengrundfläche Labor"]
    schritt_dictionary["Personlabedarf Facharbeiter"] = df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = 0
    schritt_dictionary["Investition"] = 0
    
    return schritt_dictionary

def MiKal_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
     
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = math.ceil(process.Anlagen_Anode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))
    process.Anlagen_Kathode = math.ceil(process.Anlagen_Kathode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def OptiEx(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
     
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = math.ceil(process.Anlagen_Anode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))
    process.Anlagen_Kathode = math.ceil(process.Anlagen_Kathode*(1+df["Wert"]["Leistungsaufnahme Anode"]/100))

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def ÖkoTroP_Bürstenauftrag(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def ÖkoTroP_Elektrostatisch(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    return schritt_dictionary

def HighStructures_Extrusion(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def HighStructures_Laser(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Epic(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def RollBatt(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def PräLi_Li_Salz(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PräLi_PVD(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PräLi_Opferanode(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def HoLiB_Vereinzeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    
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
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def E_Qual(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary):
    return schritt_dictionary

def ProfiStruk_Strukturierung(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def HoLiB_Stapeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = sheet_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    
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
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Cell_Fill_Separatormodifikation(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Cell_Fill_Befüllen_und_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = float(df["Wert"]["Parallelbefüllungen"])*float(df["Wert"]["Geschwindigkeit"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def FormEl(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Formierdauer"])*60/float(df["Wert"]["Anzahl Zellen/Formierturm"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    rueckgewinnungsfaktor = df["Wert"]["Rückgewinnungsfaktor"]

    Q_Z=float(Zellergebnisse["Wert"]["Ladung"]) #Speicherkapazität der Batteriezelle [Ah]
    U_OCV=float(Zellergebnisse["Wert"]["Nennspannung"]) #Klemmspannung [Volt]
    Eta_C1=float(df["Wert"]["Eta C1"]) #Coulombscher Wirkungsgrad des ersten Ladezyklus [-]
    Eta_Z=float(df["Wert"]["Eta Z"]) #Wirkungsgrad der Zelle [-]
    
    E_L1=Q_Z*U_OCV/(Eta_C1*Eta_Z) #Energiebedarf des 1. Ladevorgangs [Wh]
    E_E1=Q_Z*U_OCV #Energiebedarf des 1. Entladevorgangs [Wh]
    E_L2=Q_Z*U_OCV/Eta_Z #Energiebedarf des 2. Ladevorgangs [Wh]
    E_E2=Q_Z*U_OCV #Energiebedarf des 2. Entladevorgangs [Wh]
    E_L50=0.5*Q_Z*U_OCV/Eta_Z #Energiebedarf des letzten Ladevorgangs auf 50% SOC [Wh]
    E_FormZ=E_L1+E_L2+E_L50-(E_E1+E_E2)*rueckgewinnungsfaktor/100 #Energiebedarf Formierung einer Zelle [Wh]

    kanaele_3_monats_test = df["Wert"]["Stichproben pro Schicht 3 Monatstest"] *3*3*30 #3 Schichten pro Tag (HARDCODED) * 3 Monate * 30 Tage
    kanaele_6_monats_test = df["Wert"]["Stichproben pro Schicht 6 Monatstest"] *3*6*30 #3 Schichten pro Tag (HARDCODED) * 6 Monate * 30 Tage
    #kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"] * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"]*3 * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    lebensdauer_kanaele_gesamt = kanaele_3_monats_test + kanaele_6_monats_test + kanaele_80_cutoff_test
    anzahl_test_anlagen = math.ceil(lebensdauer_kanaele_gesamt/ df["Wert"]["Anzahl Zellen/Formierturm"])

    energiebedarf_lebensdauertest = lebensdauer_kanaele_gesamt * Q_Z * U_OCV * df["Wert"]["C-Rate Lebensdauertest"] * 0.5 * (1-rueckgewinnungsfaktor/100)*365*24 #[Wh]
    schritt_dictionary["Anzahl Maschinen"] = "{} Anlagen, {} Testanlagen".format(process.Anlagen,anzahl_test_anlagen)
    
    process.Anlagen = process.Anlagen + anzahl_test_anlagen

    

    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 + energiebedarf_lebensdauertest/1000 #[kWh]
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary



#Prozesse fürs Paper

#PHEV 2 Produktion

def PHEV2_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
     
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = math.ceil(process.Anlagen_Anode*(1+df["Wert"]["Überkapazität"]/100))
    process.Anlagen_Kathode = math.ceil(process.Anlagen_Kathode*(1+df["Wert"]["Überkapazität"]/100))

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    return schritt_dictionary

def PHEV2_Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = Anlagengrundfläche_Anode*(1-float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(1-float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]

    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode*(float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]
    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen_Anode+process.Anlagen_Kathode
    schritt_dictionary = process.investition(schritt_dictionary)
    
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def PHEV2_Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    #schritt_dictionary = process.anlagen(schritt_dictionary)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Anodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
    Kathodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
    Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)

    Geschwindigkeit_Anode = float(df["Wert"]["Geschwindigkeit Anode"])/(read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    Geschwindigkeit_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])/(read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    
    meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    
    Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/Geschwindigkeit_Anode #[min]
    Verlust_durch_Nebenzeit_Anode = df["Wert"]["Nebenzeit Anode"]/Zeit_pro_Coil_Anode #[%]
    
    Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/Geschwindigkeit_Kathode
    Verlust_durch_Nebenzeit_Kathode = float(df["Wert"]["Nebenzeit Kathode"])/Zeit_pro_Coil_Kathode #[%]
    
    Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/Geschwindigkeit_Anode*(1+Verlust_durch_Nebenzeit_Anode))
    Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/Geschwindigkeit_Kathode*(1+Verlust_durch_Nebenzeit_Kathode))

    Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Anzahl Maschinen"] = Anz_Maschinen

    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Flachwickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)   
    
    #laenge_anodensheet = Zellergebnisse["Wert"]["Sheets/ Meter Anode"]*Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"] #[m/Zelle]
    laenge_anodensheet = Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"]*Zellergebnisse["Wert"]["Sheets/ Meter Anode"]  
    Zellen_pro_Minute = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr/24/60 #[Zellen/min]

    #Meter_Anode_pro_minute = laenge_anodensheet * Zellen_pro_Minute #[m/min]
    Kapazitaet_Anlage = df["Wert"]["Geschwindigkeit"]/laenge_anodensheet #[Zellen/min]
    Zeit_pro_Zelle = 1/Kapazitaet_Anlage
    Zeit_pro_Zelle_mit_nebenzeit = Zeit_pro_Zelle+df["Wert"]["Nebenzeit"]
    Kapazitaet_Anlage_mit_nebenzeit = 1/Zeit_pro_Zelle_mit_nebenzeit

    process.Anlagen = math.ceil(Zellen_pro_Minute/Kapazitaet_Anlage_mit_nebenzeit)

    schritt_dictionary["Personlabedarf Facharbeiter"] = process.Anlagen*df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = process.Anlagen*df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = process.Anlagen*df["Wert"]["Leistungsaufnahme"]*arbeitstage_pro_jahr*24

    process.Anlagen = math.ceil(process.Anlagen * (1+df["Wert"]["Überkapazität"]/100))

    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen
    schritt_dictionary["Flächenbedarf"] = process.Anlagen*df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Trockenraum"]

    schritt_dictionary["Investition"] = process.Anlagen*df["Wert"]["Investition"]

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def PHEV2_In_Gehäuse_einführen_und_Deckelmontage(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Hülle")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = float(df["Wert"]["Parallelbefüllungen"])*float(df["Wert"]["Geschwindigkeit"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Benetzungsdauer"])*60/float(df["Wert"]["Zellen pro Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def PHEV2_Formieren_und_Entgasen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Formierdauer"])*60/float(df["Wert"]["Anzahl Zellen/Formierturm"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    rueckgewinnungsfaktor = df["Wert"]["Rückgewinnungsfaktor"]

    Q_Z=float(Zellergebnisse["Wert"]["Ladung"]) #Speicherkapazität der Batteriezelle [Ah]
    U_OCV=float(Zellergebnisse["Wert"]["Nennspannung"]) #Klemmspannung [Volt]
    Eta_C1=float(df["Wert"]["Eta C1"]) #Coulombscher Wirkungsgrad des ersten Ladezyklus [-]
    Eta_Z=float(df["Wert"]["Eta Z"]) #Wirkungsgrad der Zelle [-]
    
    E_L1=Q_Z*U_OCV/(Eta_C1*Eta_Z) #Energiebedarf des 1. Ladevorgangs [Wh]
    E_E1=Q_Z*U_OCV #Energiebedarf des 1. Entladevorgangs [Wh]
    E_L2=Q_Z*U_OCV/Eta_Z #Energiebedarf des 2. Ladevorgangs [Wh]
    E_E2=Q_Z*U_OCV #Energiebedarf des 2. Entladevorgangs [Wh]
    E_L50=0.5*Q_Z*U_OCV/Eta_Z #Energiebedarf des letzten Ladevorgangs auf 50% SOC [Wh]
    E_FormZ=E_L1+E_L2+E_L50-(E_E1+E_E2)*rueckgewinnungsfaktor/100 #Energiebedarf Formierung einer Zelle [Wh]

    kanaele_3_monats_test = df["Wert"]["Stichproben pro Schicht 3 Monatstest"] *3*3*30 #3 Schichten pro Tag (HARDCODED) * 3 Monate * 30 Tage
    kanaele_6_monats_test = df["Wert"]["Stichproben pro Schicht 6 Monatstest"] *3*6*30 #3 Schichten pro Tag (HARDCODED) * 6 Monate * 30 Tage
    #kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"] * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"]*3 * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    lebensdauer_kanaele_gesamt = kanaele_3_monats_test + kanaele_6_monats_test + kanaele_80_cutoff_test
    anzahl_test_anlagen = math.ceil(lebensdauer_kanaele_gesamt/ df["Wert"]["Anzahl Zellen/Formierturm"])

    energiebedarf_lebensdauertest = lebensdauer_kanaele_gesamt * Q_Z * U_OCV * df["Wert"]["C-Rate Lebensdauertest"] * 0.5 * (1-rueckgewinnungsfaktor/100)*365*24 #[Wh]
    schritt_dictionary["Anzahl Maschinen"] = "{} Anlagen, {} Testanlagen".format(process.Anlagen,anzahl_test_anlagen)
    
    process.Anlagen = process.Anlagen + anzahl_test_anlagen

    

    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 + energiebedarf_lebensdauertest/1000 #[kWh]
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def PHEV2_Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary
    
def PHEV2_Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Reifelagerdauer"])*24*60/float(df["Wert"]["Anzahl Zellen/Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def PHEV2_Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def PHEV2_Verpackung_und_Versand(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    schritt_dictionary["Anzahl Maschinen"] = 0
    schritt_dictionary["Flächenbedarf"] = df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = df["Wert"]["Anlagengrundfläche Trockenraum"]
    schritt_dictionary["Flächenbedarf Labor"] = df["Wert"]["Anlagengrundfläche Labor"]
    schritt_dictionary["Personlabedarf Facharbeiter"] = df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = 0
    schritt_dictionary["Investition"] = 0
    
    return schritt_dictionary


#Tesla 4680 Produktion

def Tesla_Mischen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = suspension_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
        
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Liter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Anodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Anodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Anode"]/100))/1000 #[l]
    Liter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Gewicht Kathodenbeschichtung"]/Zellergebnisse["Wert"]["Gesamtdichte Kathodenbeschichtung"]*(1/(Zellchemie["Wert"]["Feststoffgehalt Kathode"]/100))/1000 #[l]

    Anlagen_Anode = math.ceil((Liter_Anode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Anode"]))*float(df["Wert"]["Mischzeit Anode"])/(24*60))
    Anlagen_Kathode = math.ceil((Liter_Kathode_pro_Tag/float(df["Wert"]["Arbeitsvolumen Kathode"]))*float(df["Wert"]["Mischzeit Kathode"])/(24*60))
    
    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Energiebedarf"] = (Anlagen_Anode*float(df["Wert"]["Leistungsaufnahme Anode"])+Anlagen_Kathode*float(df["Wert"]["Leistungsaufnahme Kathode"]))*24*arbeitstage_pro_jahr
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)

    process.Anlagen_Anode = process.Anlagen_Anode*(1+df["Wert"]["Überkapazität"]/100)
    process.Anlagen_Kathode = process.Anlagen_Kathode*(1+df["Wert"]["Überkapazität"]/100)

    Anlagen_Dosierer_Anode = math.ceil(Anlagen_Anode/float(df["Wert"]["Anzahl Anoden-Mischer pro Dosierer"]))
    Anlagen_Dosierer_Kathode = math.ceil(Anlagen_Kathode/float(df["Wert"]["Anzahl Kathoden-Mischer pro Dosierer"]))

    schritt_dictionary["Anzahl Maschinen"] = "{} Mischer Anode, {} -Kathode, {} Dosierer Anode, {} -Kathode".format(Anlagen_Anode,Anlagen_Kathode,Anlagen_Dosierer_Anode,Anlagen_Dosierer_Kathode)

    Anzahl_Anlagen = Anlagen_Anode+Anlagen_Kathode
    
    schritt_dictionary["Investition"] =   Anlagen_Anode *float(df["Wert"]["Investition Anode"]) +\
                    Anlagen_Kathode *float(df["Wert"]["Investition Kathode"])+\
                    Anlagen_Dosierer_Anode*float(df["Wert"]["Investition Anoden-Dosierer"])+\
                    Anlagen_Dosierer_Kathode*float(df["Wert"]["Investition Kathoden-Dosierer"])
                    
    schritt_dictionary["Flächenbedarf"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Dosierer"])

    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen_Anode*float(df["Wert"]["Anlagengrundfläche Trockenraum Anode"]) +\
                                          process.Anlagen_Kathode*float(df["Wert"]["Anlagengrundfläche Trockenraum Kathode"]) +\
                                         (Anlagen_Dosierer_Anode+Anlagen_Dosierer_Kathode)*float(df["Wert"]["Anlagengrundfläche Trockenraum Dosierer"])

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenbeschichtung;Kathodenbeschichtung")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Beschichten(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    return schritt_dictionary

def Tesla_Beschichten_und_Trocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    
    Trocknerlänge_Anode = float(df["Wert"]["Geschwindigkeit Anode"])*float(df["Wert"]["Trocknungsdauer Anode"]) #[m]
    Trocknerlänge_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])*float(df["Wert"]["Trocknungsdauer Kathode"]) #[m]
    
    Anlagengrundfläche_Anode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Anode) #[m²]
    Anlagengrundfläche_Kathode = df["Wert"]["Breite Beschichtungsanlage"]*(df["Wert"]["Länge des Auftragswerks"]+Trocknerlänge_Kathode) #[m2]
    
    schritt_dictionary["Flächenbedarf"] = Anlagengrundfläche_Anode*(1-float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(1-float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]

    schritt_dictionary["Flächenbedarf Trockenraum"]  = Anlagengrundfläche_Anode*(float(df["Wert"]["Faktor Trockenraum Anode"]))*process.Anlagen_Anode+\
                                          Anlagengrundfläche_Kathode*(float(df["Wert"]["Faktor Trockenraum Kathode"]))*process.Anlagen_Anode #[m²]
    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen_Anode+process.Anlagen_Kathode
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Anodenkollektor;Kathodenkollektor")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def Tesla_Kalandrieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def Tesla_Längsschneiden(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)   
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Nachtrocknen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)
    #schritt_dictionary = process.anlagen(schritt_dictionary)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr

    Anodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Anode"].index.tolist()[0]
    Kathodenkollektorfolie = Zellchemie.loc[Zellchemie['Kategorie'] == "Kollektorfolie Kathode"].index.tolist()[0]

    Meter_Anode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"] #[m]
    Meter_Kathode_pro_Tag = Zellen_pro_Tag*Zellergebnisse["Wert"]["Anzahl Wiederholeinheiten"]/Zellergebnisse["Wert"]["Sheets/ Meter Kathode"] #[m]

    Meter_Anode_pro_Minute = Meter_Anode_pro_Tag/(24*60)
    Meter_Kathode_pro_Minute = Meter_Kathode_pro_Tag/(24*60)

    Geschwindigkeit_Anode = float(df["Wert"]["Geschwindigkeit Anode"])/(read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    Geschwindigkeit_Kathode = float(df["Wert"]["Geschwindigkeit Kathode"])/(read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Breite"]/1000)/(8*60)
    
    meter_anodenkollektorfolie_pro_rolle = read_zellinfo(Anodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    meter_kathodenkollektorfolie_pro_rolle = read_zellinfo(Kathodenkollektorfolie,Materialinfos)["Wert"]["Rollenlänge"]
    
    Zeit_pro_Coil_Anode = meter_anodenkollektorfolie_pro_rolle/Geschwindigkeit_Anode #[min]
    Verlust_durch_Nebenzeit_Anode = df["Wert"]["Nebenzeit Anode"]/Zeit_pro_Coil_Anode #[%]
    
    Zeit_pro_Coil_Kathode = meter_kathodenkollektorfolie_pro_rolle/Geschwindigkeit_Kathode
    Verlust_durch_Nebenzeit_Kathode = float(df["Wert"]["Nebenzeit Kathode"])/Zeit_pro_Coil_Kathode #[%]
    
    Anlagen_Anode = math.ceil(Meter_Anode_pro_Minute/Geschwindigkeit_Anode*(1+Verlust_durch_Nebenzeit_Anode))
    Anlagen_Kathode = math.ceil(Meter_Kathode_pro_Minute/Geschwindigkeit_Kathode*(1+Verlust_durch_Nebenzeit_Kathode))

    Anz_Maschinen = "{} Anode, {} Kathode".format(Anlagen_Anode,Anlagen_Kathode)

    process.Anlagen_Anode = Anlagen_Anode
    process.Anlagen_Kathode = Anlagen_Kathode

    schritt_dictionary["Anzahl Maschinen"] = Anz_Maschinen

    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen_getrennt(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary


def Tesla_Wickeln(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = coil_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.fixausschuss(schritt_dictionary,rueckgewinnung)   
    
    #laenge_anodensheet = Zellergebnisse["Wert"]["Sheets/ Meter Anode"]*Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"] #[m/Zelle]
    laenge_anodensheet = Zellergebnisse["Wert"]["Beschichtete Bahnen Anode"]/Zellergebnisse["Wert"]["Sheets/ Meter Anode"]
    Zellen_pro_Minute = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr/24/60 #[Zellen/min]

    #Meter_Anode_pro_minute = laenge_anodensheet * Zellen_pro_Minute #[m/min]
    Kapazitaet_Anlage = df["Wert"]["Geschwindigkeit"]/laenge_anodensheet #[Zellen/min]
    Zeit_pro_Zelle = 1/Kapazitaet_Anlage
    Zeit_pro_Zelle_mit_nebenzeit = Zeit_pro_Zelle+df["Wert"]["Nebenzeit"]
    Kapazitaet_Anlage_mit_nebenzeit = 1/Zeit_pro_Zelle_mit_nebenzeit

    process.Anlagen = math.ceil(Zellen_pro_Minute/Kapazitaet_Anlage_mit_nebenzeit)

    schritt_dictionary["Personlabedarf Facharbeiter"] = process.Anlagen*df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = process.Anlagen*df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = process.Anlagen*df["Wert"]["Leistungsaufnahme"]*arbeitstage_pro_jahr*24

    process.Anlagen = math.ceil(process.Anlagen * (1+df["Wert"]["Überkapazität"]/100))

    schritt_dictionary["Anzahl Maschinen"] = process.Anlagen
    schritt_dictionary["Flächenbedarf"] = process.Anlagen*df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Trockenraum"]

    schritt_dictionary["Investition"] = process.Anlagen*df["Wert"]["Investition"]

    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Separator")
    schritt_dictionary["Flächenbedarf Labor"] = 0

    return schritt_dictionary

def Tesla_In_Gehäuse_einführen_und_Deckelmontage(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Hülle")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Kontaktieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Elektrolyt_dosieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = float(df["Wert"]["Parallelbefüllungen"])*float(df["Wert"]["Geschwindigkeit"])
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)
    
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary,"Elektrolyt")
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Benetzen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    
    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+df["Wert"]["Nebenzeit"])
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Benetzungsdauer"])*60/float(df["Wert"]["Zellen pro Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = 0
    
    return schritt_dictionary

def Tesla_Formieren_und_Entgasen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Formierdauer"])*60/float(df["Wert"]["Anzahl Zellen/Formierturm"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    rueckgewinnungsfaktor = df["Wert"]["Rückgewinnungsfaktor"]

    Q_Z=float(Zellergebnisse["Wert"]["Ladung"]) #Speicherkapazität der Batteriezelle [Ah]
    U_OCV=float(Zellergebnisse["Wert"]["Nennspannung"]) #Klemmspannung [Volt]
    Eta_C1=float(df["Wert"]["Eta C1"]) #Coulombscher Wirkungsgrad des ersten Ladezyklus [-]
    Eta_Z=float(df["Wert"]["Eta Z"]) #Wirkungsgrad der Zelle [-]
    
    E_L1=Q_Z*U_OCV/(Eta_C1*Eta_Z) #Energiebedarf des 1. Ladevorgangs [Wh]
    E_E1=Q_Z*U_OCV #Energiebedarf des 1. Entladevorgangs [Wh]
    E_L2=Q_Z*U_OCV/Eta_Z #Energiebedarf des 2. Ladevorgangs [Wh]
    E_E2=Q_Z*U_OCV #Energiebedarf des 2. Entladevorgangs [Wh]
    E_L50=0.5*Q_Z*U_OCV/Eta_Z #Energiebedarf des letzten Ladevorgangs auf 50% SOC [Wh]
    E_FormZ=E_L1+E_L2+E_L50-(E_E1+E_E2)*rueckgewinnungsfaktor/100 #Energiebedarf Formierung einer Zelle [Wh]

    kanaele_3_monats_test = df["Wert"]["Stichproben pro Schicht 3 Monatstest"] *3*3*30 #3 Schichten pro Tag (HARDCODED) * 3 Monate * 30 Tage
    kanaele_6_monats_test = df["Wert"]["Stichproben pro Schicht 6 Monatstest"] *3*6*30 #3 Schichten pro Tag (HARDCODED) * 6 Monate * 30 Tage
    #kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"] * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    kanaele_80_cutoff_test = df["Wert"]["Stichproben pro Schicht Cutoff"]*3 * 2/df["Wert"]["C-Rate Lebensdauertest"]*df["Wert"]["Zyklenzahl"]/24
    lebensdauer_kanaele_gesamt = kanaele_3_monats_test + kanaele_6_monats_test + kanaele_80_cutoff_test
    anzahl_test_anlagen = math.ceil(lebensdauer_kanaele_gesamt/ df["Wert"]["Anzahl Zellen/Formierturm"])
    print("anzahl_test_anlagen")
    print(anzahl_test_anlagen)
    energiebedarf_lebensdauertest = lebensdauer_kanaele_gesamt * Q_Z * U_OCV * df["Wert"]["C-Rate Lebensdauertest"] * 0.5 * (1-rueckgewinnungsfaktor/100)*365*24 #[Wh]

    process.Anlagen = process.Anlagen + anzahl_test_anlagen

    schritt_dictionary["Energiebedarf"]=E_FormZ*schritt_dictionary["Zelläquivalent"]/1000 + energiebedarf_lebensdauertest/1000 #[kWh]
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def Tesla_Befüllöffnung_verschließen(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary
    
def Tesla_Reifelagern(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)

    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)

    Zellen_pro_Tag = schritt_dictionary["Zelläquivalent"]/arbeitstage_pro_jahr
    Zellen_pro_Minute = Zellen_pro_Tag/(24*60) 
    Zellen_pro_Minute = 1/(1/Zellen_pro_Minute+float(df["Wert"]["Nebenzeit"]))
    Durchsatz_pro_Minute = 1/(float(df["Wert"]["Reifelagerdauer"])*24*60/float(df["Wert"]["Anzahl Zellen/Anlage"]))
    process.Anlagen = math.ceil(Zellen_pro_Minute/Durchsatz_pro_Minute)

    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)    
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def Tesla_Prüfen_und_Klassifizieren(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    process = zelle_prozessschritt(df,Zellergebnisse,Zellchemie,Materialinfos,rueckgewinnung)
    schritt_dictionary = process.variabler_aussschuss(schritt_dictionary)
    schritt_dictionary = process.rueckgewinnung(schritt_dictionary,rueckgewinnung)
    schritt_dictionary = process.anlagen(schritt_dictionary)
    schritt_dictionary = process.mitarbeiter_anlagen(schritt_dictionary)
    schritt_dictionary = process.energie(schritt_dictionary)
    schritt_dictionary = process.ueberkapazitaet(schritt_dictionary)
    schritt_dictionary = process.flaechen(schritt_dictionary)
    schritt_dictionary = process.investition(schritt_dictionary)
    schritt_dictionary = process.neue_materialien(schritt_dictionary)
    schritt_dictionary["Flächenbedarf Labor"] = process.Anlagen*df["Wert"]["Anlagengrundfläche Labor"]
    
    return schritt_dictionary

def Tesla_Verpackung_und_Versand(df,Zellergebnisse,Zellchemie,Materialinfos,schritt_dictionary,rueckgewinnung):
    schritt_dictionary["Anzahl Maschinen"] = 0
    schritt_dictionary["Flächenbedarf"] = df["Wert"]["Anlagengrundfläche"]
    schritt_dictionary["Flächenbedarf Trockenraum"] = df["Wert"]["Anlagengrundfläche Trockenraum"]
    schritt_dictionary["Flächenbedarf Labor"] = df["Wert"]["Anlagengrundfläche Labor"]
    schritt_dictionary["Personlabedarf Facharbeiter"] = df["Wert"]["Personal Facharbeiter"]
    schritt_dictionary["Personalbedarf Hilfskraft"] = df["Wert"]["Personal Hilfskräfte"]
    schritt_dictionary["Energiebedarf"] = 0
    schritt_dictionary["Investition"] = 0
    
    return schritt_dictionary
