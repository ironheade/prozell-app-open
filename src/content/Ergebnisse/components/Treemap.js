import { TreemapChart } from "@carbon/charts-react"
import React from "react"

export default function Treemap(props) {


    const flaechen_normalraum = JSON.parse(props.ergebnisTabelle).filter(item => item.index === "Flächenbedarf")[0]
    const flaechen_trockenraum = JSON.parse(props.ergebnisTabelle).filter(item => item.index === "Flächenbedarf Trockenraum")[0]
    const anzahl_maschinen = JSON.parse(props.ergebnisTabelle).filter(item => item.index === "Anzahl Maschinen")[0]

    const children_normalraum = Object.keys(flaechen_normalraum).filter(item => item !== "index" && item !== "Einheit" && flaechen_normalraum[item] !== 0).map(item => 
        ({"name":item+" (Anlagen: "+anzahl_maschinen[item]+")",
        "value":flaechen_normalraum[item],
        "showLabel": true
    }))

    const children_trockenraum = Object.keys(flaechen_trockenraum).filter(item => item !== "index" && item !== "Einheit" && flaechen_trockenraum[item] !== 0).map(item => 
        ({"name":item+" (Anlagen: "+anzahl_maschinen[item]+")",
        "value":flaechen_trockenraum[item],
        "showLabel": true
    }))


    const flaechenverteilung_produktion = [
        {
            "name":"Normalraum",
            "children": children_normalraum
        },
        {
            "name":"Trockenraum",
            "children": children_trockenraum
        }
    ]

    const flaechenverteilung_gesamt = []
    props.data.map(item => flaechenverteilung_gesamt.push(
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
            <TreemapChart data={flaechenverteilung_gesamt} options={{title:"Flächenverteilung Grundstück",...options}} />
            <TreemapChart data={flaechenverteilung_produktion} options={{title:"Flächenverteilung Produktion",...options}} />
        </>
    )
}