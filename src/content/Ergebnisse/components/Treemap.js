import { TreemapChart } from "@carbon/charts-react"
import React from "react"

export default function Treemap(props) {

    const data = []
    props.data.map(item => data.push(
        {
            "name": item["name"],
            "children": item["children"].map(item => ({
                "name": item["name"],
                "value": item["value"],
                "showLabel": true
            }))
        }
    ))


    const options = {
        "title": "Flächenverteilung",
        "height": "400px",
        "legend": {
            "truncation": {
                "numCharacter": 45,
            }
        },
        "baseTooltop":{
            "truncation": {
                "numCharacter": 45,
            }
        }
    }

    return (
        <>
            <TreemapChart data={data} options={options} />
        </>
    )
}