# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:47:24 2022

@author: bendzuck
"""


#flaeche_normalraum = 6619
#flaeche_trockenraum = 790

def flaechenberechnung(flaeche_normalraum,flaeche_trockenraum,Gebaeude,Oekonomische_Parameter,flaeche_labor):

    #Paramter
    Zinssatz_kapitalmarkt = Oekonomische_Parameter["Wert"]["Kapitalkosten"] #[%]
    
    nutzungsdauer_gebaeude = Gebaeude["Wert"]["Nutzungsdauer"] #[Jahre]
    
    
    anlagengrundflaeche = flaeche_normalraum + flaeche_trockenraum + flaeche_labor
    
    #Produktionsfläche
    maschinenplatz_flaeche_prozent = Gebaeude["Wert"]["Maschinenplatzfläche"] #[%]
    zwischenlager_flaeche_prozent = Gebaeude["Wert"]["Zwischenlagerflächen"] #[%]
    zusatz_flaeche_prozent = Gebaeude["Wert"]["Zusatzfläche"] #[%]
    quadratmeter_preis_trockenraum = Gebaeude["Wert"]["Baukosten Trockenraum"] #[€/m²]
    quadratmeter_preis_labor = Gebaeude["Wert"]["Baukosten Labor"] #[€/m²]
    
    #Nutzfläche
    verwaltungs_flaeche_prozent = Gebaeude["Wert"]["Verwaltungsflächen"] #[%]
    lager_versand_flaeche_prozent = Gebaeude["Wert"]["Lagerflächen"] #[%]
    
    #Gebäudefläche
    neben_funktions_sozial_flaeche_prozent = Gebaeude["Wert"]["Nebenflächen"] #[%]
    quadratmeter_preis_gebaeude = Gebaeude["Wert"]["Baukosten Fabrik"] #[€/m²]
    
    #Grunstücksffläche
    zusatzfaktor_grundstueck_prozent = Gebaeude["Wert"]["Unbebaute Flächen Faktor"] #[%]
    quadratmeter_preis_grundstueck = Gebaeude["Wert"]["Preis Grundstück"] #[€/m²]
    
    
    #Berechnung Produktionsfläche
    
    #produktionsflaeche =  anlagengrundflaeche*(1+(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent)/(100-(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent)))
    produktionsflaeche =  anlagengrundflaeche/(100-(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent))

    maschinenplatz_flaeche = maschinenplatz_flaeche_prozent*produktionsflaeche/100
    zwischenlager_flaeche = zwischenlager_flaeche_prozent*produktionsflaeche/100
    zusatz_flaeche = zusatz_flaeche_prozent/100*produktionsflaeche
    
    
    #Berechnung Nutzfläche
    
    #nutzflaeche =  produktionsflaeche*(1+(verwaltungs_flaeche_prozent+lager_versand_flaeche_prozent)/(100-(verwaltungs_flaeche_prozent+lager_versand_flaeche_prozent)))
    nutzflaeche =  produktionsflaeche/(100-(verwaltungs_flaeche_prozent+lager_versand_flaeche_prozent))
    verwaltungs_flaeche = verwaltungs_flaeche_prozent*nutzflaeche/100
    lager_versand_flaeche = lager_versand_flaeche_prozent*nutzflaeche/100
    
    #Berechnung Gebäudefläche
    
    #gebaeudeflaeche = nutzflaeche*(1+(neben_funktions_sozial_flaeche_prozent/(100-neben_funktions_sozial_flaeche_prozent)))
    gebaeudeflaeche = nutzflaeche/(100-neben_funktions_sozial_flaeche_prozent)
    neben_funktions_sozial_flaeche = neben_funktions_sozial_flaeche_prozent*gebaeudeflaeche/100
    
    #Berechnung Grundstücksfläche
    
    grundstuecksflaeche =  gebaeudeflaeche*(1+zusatzfaktor_grundstueck_prozent/100)
    unbebaute_flaeche = grundstuecksflaeche-gebaeudeflaeche
    
    
    
    
    investition_kosten_bau = [
        {
            "group": "Grundstückskosten",
            "value": round(grundstuecksflaeche*quadratmeter_preis_grundstueck)
        },
        {
            "group": "Fabrikkosten",
            "value": round(gebaeudeflaeche*quadratmeter_preis_gebaeude)
        },
        {
            "group": "Trockenraumkosten",
            #"value": round(flaeche_trockenraum*quadratmeter_preis_trockenraum)
            "value": round(flaeche_trockenraum/(100-(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent))*quadratmeter_preis_trockenraum)
        },
        {
            "group": "Laborkosten",
            #"value": round(flaeche_labor*quadratmeter_preis_labor)
            "value": round(flaeche_labor/(100-(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent))*quadratmeter_preis_labor)
        }
        
                              ]

    
    flaechen_verteilung = [
    
        {
            "name": "Außenflächen",
            "children": [
                {
                    "name": "Außenflächen",
                    "value": round(unbebaute_flaeche)
                }
            ]
        }, {
            "name": "Gebäudeflächen",
            "children": [
                {
                    "name": "Neben-, Funktions- und Sozialfläche",
                    "value": round(neben_funktions_sozial_flaeche)
                },
                {
                    "name": "Lager- und Versandfläche",
                    "value": round(lager_versand_flaeche)
                },
                {
                    "name": "Verwaltungsfläche",
                    "value": round(verwaltungs_flaeche)
                }
            ]
        }, {
            "name": "Produktionsflächen",
            "children": [
                {
                    "name": "Zusatzfläche",
                    "value": round(zusatz_flaeche)
                },
                {
                    "name": "Zwischenlagerfläche",
                    "value": round(zwischenlager_flaeche)
                },
                {
                    "name": "Maschinenplatzfläche",
                    "value": round(maschinenplatz_flaeche)
                },
                {
                    "name": "Anlagengrundfläche Trockenraum",
                    "value": round(flaeche_trockenraum)
                },
                {
                    "name": "Anlagengrundfläche Normalraum",
                    "value": round(flaeche_normalraum)
                },
                {
                    "name": "Anlagengrundfläche Labor",
                    "value": round(flaeche_labor)
                }
            ]
        }
    
    ]
    
    Fabrikflaeche = round(
        neben_funktions_sozial_flaeche+
        lager_versand_flaeche+
        verwaltungs_flaeche+
        zusatz_flaeche+
        zwischenlager_flaeche+
        maschinenplatz_flaeche+
        flaeche_trockenraum+
        flaeche_normalraum+
        flaeche_labor
    )
    
    #Fabrikflaeche_ohne_Produktion = round(
    #    Fabrikflaeche-
    #    flaeche_trockenraum-
    #    flaeche_normalraum-
    #    flaeche_labor
    #)

    Fabrikflaeche_ohne_Produktion = round(Fabrikflaeche-produktionsflaeche)
    
    jaehrliche_flaechenkosten = quadratmeter_preis_gebaeude*Zinssatz_kapitalmarkt/100+quadratmeter_preis_gebaeude/nutzungsdauer_gebaeude
    #+quadratmeter_preis_gebaeude/100
    
    return investition_kosten_bau, flaechen_verteilung, jaehrliche_flaechenkosten, Fabrikflaeche, Fabrikflaeche_ohne_Produktion
    

#flaechenberechnung(flaeche_normalraum,flaeche_trockenraum)