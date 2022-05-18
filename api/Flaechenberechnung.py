# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:47:24 2022

@author: bendzuck
"""


flaeche_normalraum = 6619
flaeche_trockenraum = 790

def flaechenberechnung(flaeche_normalraum,flaeche_trockenraum,Gebaeude,Oekonomische_Parameter):

    #Paramter
    Zinssatz_kapitalmarkt = Oekonomische_Parameter["Wert"]["Zinssatz Kapitalmarkt"] #[%]
    
    nutzungsdauer_gebaeude = Gebaeude["Wert"]["Nutzungsdauer"] #[Jahre]
    
    
    anlagengrundflaeche = flaeche_normalraum + flaeche_trockenraum
    
    #Produktionsfläche
    maschinenplatz_flaeche_prozent = Gebaeude["Wert"]["Maschinenplatzfläche"] #[%]
    zwischenlager_flaeche_prozent = Gebaeude["Wert"]["Zwischenlagerflächen"] #[%]
    zusatz_flaeche_prozent = Gebaeude["Wert"]["Zusatzfläche"] #[%]
    quadratmeter_preis_trockenraum = Gebaeude["Wert"]["Baukosten Trockenraum"] #[€/m²]
    
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
    
    produktionsflaeche =  anlagengrundflaeche*(1+(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent)/(100-(maschinenplatz_flaeche_prozent+zwischenlager_flaeche_prozent+zusatz_flaeche_prozent)))
    
    maschinenplatz_flaeche = maschinenplatz_flaeche_prozent*produktionsflaeche/100
    zwischenlager_flaeche = zwischenlager_flaeche_prozent*produktionsflaeche/100
    zusatz_flaeche = zusatz_flaeche_prozent/100*produktionsflaeche
    
    
    #Berechnung Nutzfläche
    
    nutzflaeche =  produktionsflaeche*(1+(verwaltungs_flaeche_prozent+lager_versand_flaeche_prozent)/(100-(verwaltungs_flaeche_prozent+lager_versand_flaeche_prozent)))
    verwaltungs_flaeche = verwaltungs_flaeche_prozent*nutzflaeche/100
    lager_versand_flaeche = lager_versand_flaeche_prozent*nutzflaeche/100
    
    #Berechnung Gebäudefläche
    
    gebaeudeflaeche = nutzflaeche*(1+(neben_funktions_sozial_flaeche_prozent/(100-neben_funktions_sozial_flaeche_prozent)))
    neben_funktions_sozial_flaeche = neben_funktions_sozial_flaeche_prozent*gebaeudeflaeche/100
    
    #Berechnung Grundstücksfläche
    
    grundstuecksflaeche =  gebaeudeflaeche*(1+zusatzfaktor_grundstueck_prozent/100)
    unbebaute_flaeche = grundstuecksflaeche-gebaeudeflaeche
    
    
    
    investition_kosten_bau_alt = {"Grundstückskosten":round(grundstuecksflaeche*quadratmeter_preis_grundstueck),
                           "Fabrikkosten":round(gebaeudeflaeche*quadratmeter_preis_gebaeude),
                           "Trockenraumkosten":round(flaeche_trockenraum*quadratmeter_preis_trockenraum)}
    
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
            "value": round(flaeche_trockenraum*quadratmeter_preis_trockenraum)
        }
                              ]
    
    
    {"Grundstückskosten":round(grundstuecksflaeche*quadratmeter_preis_grundstueck),
                           "Fabrikkosten":round(gebaeudeflaeche*quadratmeter_preis_gebaeude),
                           "Trockenraumkosten":round(flaeche_trockenraum*quadratmeter_preis_trockenraum)}
    
    
    flaechen_verteilung_alt = {"Anlagengrundfläche Normalraum":round(flaeche_normalraum),
                           "Anlagengrundfläche Trockenraum":round(flaeche_trockenraum),
                           "Maschinenplatzfläche":round(maschinenplatz_flaeche),
                           "Zwischenlagerfläche":round(zwischenlager_flaeche),
                           "Zusatzfläche":round(zusatz_flaeche),
                           "Verwaltungsfläche":round(verwaltungs_flaeche),
                           "Lager- und Versandfläche":round(lager_versand_flaeche),
                           "Neben-, Funktions- und Sozialfläche":round(neben_funktions_sozial_flaeche),
                           "Unbebaute Fläche":round(unbebaute_flaeche),
                           }
    
    
    flaechen_verteilung = [
    
        {
            "name": "Außenflächen",
            "children": [
                {
                    "name": "Unbebaute Fläche",
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
            "name": "Produktionsfflächen",
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
                }
            ]
        }
    
    ]
    
    
    jaehrliche_flaechenkosten = quadratmeter_preis_gebaeude*Zinssatz_kapitalmarkt/200+quadratmeter_preis_gebaeude/nutzungsdauer_gebaeude+quadratmeter_preis_gebaeude/100
    
    return investition_kosten_bau, flaechen_verteilung, jaehrliche_flaechenkosten
    

#flaechenberechnung(flaeche_normalraum,flaeche_trockenraum)