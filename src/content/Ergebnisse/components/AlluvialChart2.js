import { AlluvialChart } from "@carbon/charts-react";
import React from 'react'

export default function Alluvial2(){
    const Data=[
        {
            "source": "About Modal",
            "target": "Automation",
            "value": 1
        }
    ]
    const Options = {
        "alluvial": {
            "nodes": [
                {
                    "name": "About Modal",
                    "category": "Pattern"
                },
                {
                    "name": "Automation",
                    "category": "Group"
                }
            ]
        },
        "color": {
            "scale": {
                "About Modal": "#da1e28",
                "Automation": "#b28600"
            },
            "gradient": {
                "enabled": true
            }
        },
        "height": "100px",
}

    return(
        <div key="alluvial">
        <AlluvialChart data={Data} options={Options}/>
        </div>
    )
}