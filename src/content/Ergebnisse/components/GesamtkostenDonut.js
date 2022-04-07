import { DonutChart } from "@carbon/charts-react";
import React from 'react'

export default function GesamtkostenDonut(props) {
    const Data = [
        {
            "group": "2V2N 9KYPM version 1",
            "value": 20000
        },
        {
            "group": "L22I P66EP L22I P66EP L22I P66EP",
            "value": 65000
        },
        {
            "group": "JQAI 2M4L1",
            "value": 75000
        },
        {
            "group": "J9DZ F37AP",
            "value": 1200
        },
        {
            "group": "YEL48 Q6XK YEL48",
            "value": 10000
        },
        {
            "group": "Misc",
            "value": 25000
        }
    ]

    const DataGesamt = [
        {
            "group": "Produktion",
            "value": 20000
        },
        {
            "group": "Overhead",
            "value": 65000
        }
    ]
    const Options = {
        "resizable": true,
        "donut": {
            "center": {
                "label": "Browsers"
            }
        },
        "height": "400px"
    }
    return (
        <>
            <div className="bx--grid bx--grid--full-width">
                <div className="bx--row">
                    <div className="bx--col-lg-5">
                        <DonutChart data={DataGesamt} options={{...Options,title: "Gesamt"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={Data} options={{...Options,title: "Produktion"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={Data} options={{...Options,title: "Overhead"}} />
                    </div>
                </div>
            </div>
        </>
    )

}