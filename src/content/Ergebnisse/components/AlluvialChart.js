import { AlluvialChart } from "@carbon/charts-react";
import React from 'react'


export default function Alluvial(props) {

    const nodes =  [
        {
            "name": "Zelle",
            "category": "Ziel"
        },
        {
            "name": "Rückgewinnung",
            "category": "Ziel"
        },
        {
            "name": "Verlust",
            "category": "Ziel"
        } 
    ]

    const rueckgewinnung = {}
    JSON.parse(props.rueckgewinnung).map(item => rueckgewinnung[item.Beschreibung]=item.Wert)
    const data = []
    props.data !== null && props.data.map(item => 
        data.push({...item,rueckgewinnung:rueckgewinnung[item.Material]})
        )
    const DataMaterial = []
    data.map(item =>
        DataMaterial.push(
            {
                "source": item.Material,
                "target": "Zelle",
                "value": Math.round(item.Zelle/item.Gesamt*props.data_kosten[item.Material])
            },
            {
                "source": item.Material,
                "target": "Rückgewinnung",
                "value": Math.round(((item.Gesamt-item.Zelle)/item.Gesamt)*item.rueckgewinnung/100*props.data_kosten[item.Material])
            },
            {
                "source": item.Material,
                "target": "Verlust",
                "value": Math.round(((item.Gesamt-item.Zelle)/item.Gesamt)*(1-item.rueckgewinnung/100)*props.data_kosten[item.Material])
            }

        ) &
        nodes.push({"name":item.Material,"category": "Ausgangsmaterial"})
        )


    const Options = {
        "alluvial": {
            "nodes": 
            
            [
                {
                    "name": "Anodenbeschichtung",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Kathodenbeschichtung",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Anodenkollektor",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Kathodenkollektor",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Separator",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Elektrolyt",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Zelle",
                    "category": "Ziel"
                },
                {
                    "name": "Rückgewinnung",
                    "category": "Ziel"
                },
                {
                    "name": "Verlust",
                    "category": "Ziel"
                }
            ]
            

        },
        "height": "600px",
/*
        "color": {

            "scale": {
                "Aktivmaterial Anode": "#da1e28",
                "Trägerfolie Kathode": "#b28600",
                "Aktivmaterial Kathode": "#198038",
                "Elektrolyt": "#ee538b",
                "Trägerfolie Anode": "#08bdba",
                "Zelle": "#1192e8",
                "Rückgewinnung": "#a56eff",
                "Verlust": "#009d9a",

            },
            
            "gradient": {
                "enabled": true
            }
        }
        */

    }


    
      
    return (
        <div className="bx--grid bx--grid--full-width">
            {DataMaterial !== [] &&
            <div className="bx--row">
                <div className="bx--col-lg-16">
                    <AlluvialChart
                        data={DataMaterial}
                        options={{ ...Options, title: "Kostenfluss in €" }}
            />

                </div>
                {/* 
                <div className="bx--col-lg-8">
                <AlluvialChart
                        data={DataMaterial2}
                        options={{ ...Options, title: "Kostenfluss" }}
                    />

                </div>
                */}
            </div>
}
        </div>
    )
}
