import { AlluvialChart } from "@carbon/charts-react";
import React from 'react'


export default function Alluvial() {

    const DataMaterial = [
        {
            "source": "Trägerfolie Kathode",
            "target": "Zelle",
            "value": 28
        },
        {
            "source": "Trägerfolie Kathode",
            "target": "Rückgewinnung",
            "value": 4
        },
        {
            "source": "Trägerfolie Kathode",
            "target": "Verlust",
            "value": 3
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Zelle",
            "value": 38
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Rückgewinnung",
            "value": 5
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Verlust",
            "value": 2
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Zelle",
            "value": 23
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Rückgewinnung",
            "value": 9
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Verlust",
            "value": 1
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Zelle",
            "value": 44
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Rückgewinnung",
            "value": 3
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Verlust",
            "value": 3
        },
        {
            "source": "Elektrolyt",
            "target": "Zelle",
            "value": 14
        },
        {
            "source": "Elektrolyt",
            "target": "Rückgewinnung",
            "value": 1
        },
        {
            "source": "Elektrolyt",
            "target": "Verlust",
            "value": 1
        }
    ]

    const DataKosten = [
        {
            "source": "Trägerfolie Kathode",
            "target": "Zelle",
            "value": 18
        },
        {
            "source": "Trägerfolie Kathode",
            "target": "Rückgewinnung",
            "value": 4
        },
        {
            "source": "Trägerfolie Kathode",
            "target": "Verlust",
            "value": 3
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Zelle",
            "value": 78
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Rückgewinnung",
            "value": 5
        },
        {
            "source": "Aktivmaterial Anode",
            "target": "Verlust",
            "value": 2
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Zelle",
            "value": 103
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Rückgewinnung",
            "value": 9
        },
        {
            "source": "Aktivmaterial Kathode",
            "target": "Verlust",
            "value": 1
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Zelle",
            "value": 24
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Rückgewinnung",
            "value": 3
        },
        {
            "source": "Trägerfolie Anode",
            "target": "Verlust",
            "value": 3
        },
        {
            "source": "Elektrolyt",
            "target": "Zelle",
            "value": 14
        },
        {
            "source": "Elektrolyt",
            "target": "Rückgewinnung",
            "value": 1
        },
        {
            "source": "Elektrolyt",
            "target": "Verlust",
            "value": 1
        }
    ]


    const Options = {
        "alluvial": {
            "nodes": [
                {
                    "name": "Trägerfolie Kathode",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Aktivmaterial Anode",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Aktivmaterial Kathode",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Elektrolyt",
                    "category": "Ausgangsmaterial"
                },
                {
                    "name": "Trägerfolie Anode",
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
    }


    
      
    return (
        <div className="bx--grid bx--grid--full-width">
            <div className="bx--row">
                <div className="bx--col-lg-8">
                    <AlluvialChart
                        data={DataMaterial}
                        options={{ ...Options, title: "Materialfluss" }}
                    />

                </div>
                <div className="bx--col-lg-8">
                <AlluvialChart
                        data={DataKosten}
                        options={{ ...Options, title: "Kostenfluss" }}
                    />

                </div>
            </div>
        </div>
    )
}
