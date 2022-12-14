import { DonutChart } from "@carbon/charts-react";
import React from 'react'
import { useSelector } from 'react-redux'

export default function GesamtkostenDonut(props) {
    const GWH_Jahr_AH_Zelle = useSelector(state => state.GWH_Jahr_AH_Zelle);
    const data = JSON.parse(props.data) //die Tabelle der Produktionsergebnisse
    const Kostenfaktoren = props.Kostenfaktoren //die betrachteten Kostenfaktoren
    const Produktionskosten = [] //die Produktionskosten aufsummiert für die Kostenfaktorens
    var Produktionskosten_gesamt = 0 //die gesamten Produktionskosten
    //const Overheadkosten = []
    var Overheadkosten_gesamt = 0
    const Materialkosten = []
    const Rückgewinnung = []

    //const levelized_cost = props.levelized_cost
    const levelized_cost = props.levelizedCost

    Object.keys(props.data_kosten).map(item =>
        Materialkosten.push({
            "group": item,
            "value": props.data_kosten[item]
        }))


    Object.keys(props.materialkosten_rueckgewinnung).map(item =>
        Rückgewinnung.push({
            "group": item,
            "value": props.materialkosten_rueckgewinnung[item]
        }))



    Kostenfaktoren.map(Kostenfaktor => //durch die Kostenfaktoren gehen
        data.map(item => item.index === Kostenfaktor && //die Zeile aus den Ergebnissen für den Kostenfaktor
            Produktionskosten.push(
                {
                    "group": item.index,
                    "value": (Object.keys(item).map(key => key !== "Einheit" && key !== "index" && item[key]).reduce((result, number) => result + number))
                })
        ))

    Produktionskosten.map(item => Produktionskosten_gesamt = Produktionskosten_gesamt + item.value) //Aufsummieren der Produktionskosten für die gesamten Produktionskosten


    const OverheadKosten = [
        {
            "group": "Personal",
            "value": 20000000
        },
        {
            "group": "Fläche",
            "value": 6500000
        },
        {
            "group": "Klimatisierung",
            "value": 7500000
        },
        {
            "group": "Steuer",
            "value": 1200000
        },
        {
            "group": "Investitions-Overhead",
            "value": 10000000
        }
    ]

    props.overheadKosten !== null && props.overheadKosten.map(item => Overheadkosten_gesamt = Overheadkosten_gesamt + item.value) //Aufsummieren der Produktionskosten für die gesamten Produktionskosten

    const Gesamtkosten = [
        {
            "group": "Produktion",
            "value": Produktionskosten_gesamt
        },
        {
            "group": "Overhead",
            "value": Overheadkosten_gesamt
        }
    ]

    const Options = {
        "resizable": true,
        "legend": {
            "truncation": {
                "numCharacter": 45,
            }
        },
        "height": "400px",
        "donut": {
            "center": {
                "label": "€/KWh",
                "numberFormatter": (number) => (Math.round(number / GWH_Jahr_AH_Zelle.GWh_pro_jahr / 10000) / 100).toLocaleString('de-DE')
            }
        }
    }

    const FlaechenOptions = {
        "resizable": true,
        "legend": {
            "truncation": {
                "numCharacter": 45,
            }
        },
        "height": "400px",
        "donut": {
            "center": {
                "label": "€",
                "numberFormatter": (number) => Math.floor(number).toLocaleString('de-DE')
            }
        }
    } 

    return (
        <>
            <div className="bx--grid bx--grid--full-width">
                <div className="bx--row">
                    <div className="bx--col-lg-5">
                        <DonutChart data={levelized_cost} options={{...Options, title: "Produktionskosten (Full Cost) ohne Rückgewinnung"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={props.levelized_cost_aufgeteilt_rueckgewinnung} options={{...Options, title: "Produktionskosten (Full Cost) mit Rückgewinnung"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={Materialkosten} options={{...Options, title: "Materialkosten ohne Rückgewinnung"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={Rückgewinnung} options={{...Options, title: "Material mit Rückgewinnung"}} />
                    </div>
                    <div className="bx--col-lg-5">
                        <DonutChart data={props.baukosten} options={{...FlaechenOptions, title: "Baukosten"}} />
                    </div>
                </div>
            </div>
        </>
    )
}