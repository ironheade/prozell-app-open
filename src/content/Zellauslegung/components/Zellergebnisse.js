import React from 'react'
import { useSelector } from 'react-redux'
import {
    TableRow,
    TableCell,
    TableBody,
    Table,
    TableHead,
    TableHeader,
    Dropdown,
    Button
  } from 'carbon-components-react';
import { StackedAreaChart, DonutChart } from "@carbon/charts-react";
import "@carbon/charts/styles.css";

const data = [
	{
		"group": "Dataset 1",
		"date": "2018-12-31T23:00:00.000Z",
		"value": 10000
	},
	{
		"group": "Dataset 1",
		"date": "2019-01-04T23:00:00.000Z",
		"value": 65000
	},
	{
		"group": "Dataset 1",
		"date": "2019-01-07T23:00:00.000Z",
		"value": 10000
	},
	{
		"group": "Dataset 1",
		"date": "2019-01-12T23:00:00.000Z",
		"value": 49213
	},
	{
		"group": "Dataset 1",
		"date": "2019-01-16T23:00:00.000Z",
		"value": 51213
	},
	{
		"group": "Dataset 2",
		"date": "2018-12-31T23:00:00.000Z",
		"value": 20000
	},
	{
		"group": "Dataset 2",
		"date": "2019-01-04T23:00:00.000Z",
		"value": 25000
	},
	{
		"group": "Dataset 2",
		"date": "2019-01-07T23:00:00.000Z",
		"value": 60000
	},
	{
		"group": "Dataset 2",
		"date": "2019-01-12T23:00:00.000Z",
		"value": 30213
	},
	{
		"group": "Dataset 2",
		"date": "2019-01-16T23:00:00.000Z",
		"value": 55213
	},
	{
		"group": "Dataset 3",
		"date": "2018-12-31T23:00:00.000Z",
		"value": 30000
	},
	{
		"group": "Dataset 3",
		"date": "2019-01-04T23:00:00.000Z",
		"value": 20000
	},
	{
		"group": "Dataset 3",
		"date": "2019-01-07T23:00:00.000Z",
		"value": 40000
	},
	{
		"group": "Dataset 3",
		"date": "2019-01-12T23:00:00.000Z",
		"value": 60213
	},
	{
		"group": "Dataset 3",
		"date": "2019-01-16T23:00:00.000Z",
		"value": 25213
	}
];

const options = {
	"title": "Stacked area (time series)",
	"axes": {
		"left": {
			"stacked": true,
			"scaleType": "linear",
			"mapsTo": "value"
		},
		"bottom": {
			"scaleType": "time",
			"mapsTo": "date"
		}
	},
	"curve": "curveMonotoneX",
	"height": "500px"
};



export default function Zellergebnisse(){

    const Zellergebnisse = useSelector(state => state.zellergebnisse)


    var donutData = [

    ]
    var excludeList = ["Gesamtgewicht Zelle", "Gesamtdichte Anodenbeschichtung", "Gesamtdichte Kathodenbeschichtung"]
    {Zellergebnisse !== null &&
        JSON.parse(Zellergebnisse).filter(item => item.Kategorie === "Gewichte und Dichten" && !excludeList.includes(item.Beschreibung) ).map(item =>
            donutData.push({group: item.Beschreibung, value: item.Wert})
            )
    }

/*
    const donutOptions = {
        "title": "Gewichtsverteilung Zelle",
        "resizable": true,
        "legend": {
            "hidden": true,
            "alignment": "center",
            "truncation": {
                "numCharacter": 35,
            }
          },
        "donut": {
          "center": {
            "label": "Gewicht Zelle [g]"
        },
        "alignment": "center"
        },
        "height": "400px",
        "width": "800px"
      };


    const costDonutOptions = {
        "title": "Kostenverteilung Zelle",
        "resizable": true,
        "legend": {
            "alignment": "center",
            "truncation": {
                "numCharacter": 35,
            }
          },
        "donut": {
          "center": {
            "label": "Gesamtkosten Zelle [€]"
        },
        "alignment": "center"
        },
        "height": "400px",
        "width": "800px"
      };

*/

    var costDonutData = [

    ]
    var excludeList = ["Kilopreis Anodenbeschichtung", "Kilopreis Kathodenbeschichtung", "Materialkosten einer Zelle"]
    {Zellergebnisse !== null &&
        JSON.parse(Zellergebnisse).filter(item => item.Kategorie === "Kosten" && !excludeList.includes(item.Beschreibung) ).map(item =>
            costDonutData.push({group: item.Beschreibung, value: item.Wert})
            )
    }


    const costDonutOptions = {
        "title": "Kostenverteilung Zelle",
        "resizable": true,
        "legend": {
            "position": "left",
            "orientation": "vertical",
            "truncation": {
                "numCharacter": 45,
            }
          },
        "donut": {
          "center": {
            "label": "Gesamtkosten Zelle [€]"
        },
        "alignment": "center"
        },
        "height": "400px",
        "width": "600px"
      };



    const donutOptions = {
        "title": "Gewichtsverteilung Zelle",
        "resizable": true,
        "legend": {
            "position": "left",
            "orientation": "vertical",
            "truncation": {
                "numCharacter": 45,
            }
          },
        "donut": {
          "center": {
            "label": "Gewicht Zelle [g]"
        },
        "alignment": "center"
        },
        "height": "400px",
        "width": "600px"
      };
      

    return (
        <>
            <div className="bx--col-lg-4">
            {Zellergebnisse !== null &&
                <Table useZebraStyles size="compact" className="zellchemie_table">
                    <TableHead>
                        <TableRow>
                        <TableHeader>
                        Beschreibung
                        </TableHeader>
                        <TableHeader>
                        Wert
                        </TableHeader>
                        <TableHeader>
                        Einheit     
                        </TableHeader>
                    </TableRow>
                    </TableHead>
                    
                    {[...new Set(JSON.parse(Zellergebnisse).map(item => item.Kategorie))].map(item_outer =>

                        <TableBody key={item_outer}>
                            <TableRow>
                                
                                <TableCell style={{ backgroundColor: 'black' }}><h4 style={{ color: 'white' }}>{item_outer}</h4></TableCell>
                                <TableCell style={{ backgroundColor: 'black' }}></TableCell>
                                <TableCell style={{ backgroundColor: 'black' }}></TableCell>

                            </TableRow>
                        {JSON.parse(Zellergebnisse).filter(item => item.Kategorie === item_outer).map(item => 
                            <TableRow key={item.Beschreibung}>
                                <TableCell>{item.Beschreibung}</TableCell>
                                <TableCell>{item.Wert}</TableCell>
                                <TableCell>{item.Einheit}</TableCell>

                            </TableRow>
                        
                            )}
                        </TableBody>
                    )}
                </Table>
            }
        </div>
        
        <div className="bx--col-lg-8">
            

            <h2>Graphen</h2>
                <div className="bx--row">
                    <div className="bx--col-lg-10">
                    <DonutChart
                    data={donutData}
                    options={donutOptions}
                    />
                    </div>
                    <div className="bx--col-lg-6">
                    <DonutChart
                    data={costDonutData}
                    options={costDonutOptions}
                    />
                    </div>

                </div>
            

                <div className="bx--row">
                <StackedAreaChart
                    data={data}
                    options={options}
                    />
                </div>
        </div>
        </>
    )
}