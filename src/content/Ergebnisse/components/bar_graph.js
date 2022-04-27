import React from "react";
import { StackedBarChart } from "@carbon/charts-react";




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
    //Array mit den JSON Objekten nötig für das Balkendiagramm
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


    //Array mit gerader Anzahl an Prozessschritten (Trockenraum ja, Trockenraum nein, Ja, Nein, ...)
    var dryRoomRaw = []
    JSON.parse(props.data).map(item => item.index === "Flächenbedarf Trockenraum" && dryRoomRaw.push(item))
    dryRoomRaw = dryRoomRaw[0]
    delete dryRoomRaw.index
    delete dryRoomRaw.Einheit
    const dryRoom = []

    var tempList = []
    function empty (array) {
        array.length=0
    }
    Object.keys(dryRoomRaw).map((item, index) => 
        dryRoomRaw[item] !== 0 
        ? 
        tempList.push(item)
        : 
        tempList.length !== 0 && dryRoom.push(tempList[0]) & dryRoom.push(tempList[tempList.length-1]) & empty(tempList)
    )
    tempList.length !==0 && dryRoom.push(tempList[0]) 
    tempList.length !==0 && dryRoom.push(tempList[tempList.length-1]) 

    //Bringt vorigen Array in Form: [[Ja,Nein],[Ja,Nein],...]
    const dryRoomFormiert = dryRoom.reduce(function (rows, key, index) { 
        return (index % 2 === 0 ? rows.push([key]) 
          : rows[rows.length-1].push(key)) && rows;
      }, []);

    //Erstellt Array mit JSON Objekten für die Markierung in den folgenden options
    const dryRoomArray = []
    dryRoomFormiert.map(item =>
                     
        dryRoomArray.push({
            startHighlight: item[0],
            label: "Custom formatter",
            endHighlight: item[1]
          })
        )

    const options = {
        //title: "Prozessroute",
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
                    "data": dryRoomArray                    
                  }
            },

        },

        "height": "600px"
        
    }

    return(
        <>
            <StackedBarChart
                data={data}
                options={{...options,"title":"Kosten Produktion pro Jahr"}}>
            </StackedBarChart>
            <StackedBarChart
                data={data_stacked}
                options={{...options,"title":"Kosten Produktion kummuliert pro Jahr"}}>
            </StackedBarChart>
        </>
    )
}