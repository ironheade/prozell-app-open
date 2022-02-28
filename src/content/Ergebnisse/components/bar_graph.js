import React from "react";
import { StackedBarChart } from "@carbon/charts-react";
import "@carbon/charts/styles.css";



export default function MyStackedBarChart(props){

    const Prozessroute = props.Prozessroute

    const Kostenfaktoren = [
        "Materialkosten", 
         'Personalkosten', 
         'Energiekosten', 
         'Instandhaltungskosten', 
         'Flächenkosten', 
         'Kalkulatorische Zinsen', 
         'Ökonomische Abschreibung'
    ]
    //Normales Balkendiagramm
    const data = []
    Kostenfaktoren.map(Kostenfaktor => //die Kostenfaktoren
        JSON.parse(props.data).map(item => //alle Items
            item.index === Kostenfaktor && //nur die Items (Zeilen) der Kostenfaktoren
                Prozessroute.map(prozess => //jeden Prozess durchgehen

                        data.push(
                            {
                                "group":Kostenfaktor,
                                "key":prozess,
                                "value":item[prozess]  //Wert
                            }
                        )
                    )
                )
            )

    //aufsummiertes Balkendiagramm
    const data_stacked = [                            {
        "group":"Kostenfaktor",
        "key":"prozess",
        "value":0  //Wert
    } ]
    Kostenfaktoren.map(Kostenfaktor => //die Kostenfaktoren
        JSON.parse(props.data).map(item => //alle Items
            item.index === Kostenfaktor && //nur die Items (Zeilen) der Kostenfaktoren
                Prozessroute.map(prozess => //jeden Prozess durchgehen
                    {[...data_stacked].slice(-1)[0].group !== Kostenfaktor ? //Wenn ein neuer Kostenfaktor beginnt: nicht die Werte vom vorherigen Eintrag aufsummieren
                        data_stacked.push(
                            {
                                "group":Kostenfaktor,
                                "key":prozess,
                                "value":item[prozess]  //Wert
                            } 
                        )
                        :
                        data_stacked.push(
                            {
                                "group":Kostenfaktor,
                                "key":prozess,
                                "value":item[prozess]+[...data_stacked].slice(-1)[0].value  //Wert vom vorherigen Eintrag aufsummieren
                            }
                        ) 
                    },
                )
            )
        )
        data_stacked.shift()

    const dryRoomStart = "Vereinzeln"
    const dryRoomEnd = "Befüllöffnung verschließen"

    const options = {
        "title": "Prozessroute",
        "legend": {
            "position": "left",

            "truncation": {
                "numCharacter": 45,
            }
            },
        "bars":{
            "maxWidth":120
        },
        "axes": {
            "left": {
                "mapsTo": "value",
                "stacked": true,
                "title":"Kosten [€]"
            },
            "bottom": {
                "mapsTo": "key",
                "scaleType": "labels",
                "truncation": {
                    "numCharacter": 45,
                },
                "highlights": {
                    "highlightStartMapsTo": "startHighlight",
                    "highlightEndMapsTo": "endHighlight",
                    "labelMapsTo": "label",
                    "data": [
                      {
                        "startHighlight": dryRoomStart,
                        "label": "Custom formatter",
                        "endHighlight": dryRoomEnd
                      }]
                  }
            },

        },

        "height": "600px"
        
    }
    

    return(
        <>
            <StackedBarChart
                data={data}
                options={options}>
            </StackedBarChart>
            <StackedBarChart
                data={data_stacked}
                options={options}>
            </StackedBarChart>
        </>
    )
}