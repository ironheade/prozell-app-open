import React from 'react';
import { Tooltip } from 'carbon-components-react';

export default function ProzessTooltip(props) {


    /* const tooltips = [
         {
             Dateiname: 'mischen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'multiex_mischen',
             text: 'Multiskalenansatz zur Beschreibung des Rußaufschlusses bei extrusionsbasierter Dispergierung von Lithium-Ionen-Batteriesuspensionen',
             quelle: 'https://prozell-cluster.de/projekte/multiex/'
         },
         {
             Dateiname: 'mikal_mischen',
             text: 'Optimale Elektrodenstruktur und -dichte durch integrierte Auslegung von Misch- und Kalandrierprozessen',
             quelle: 'https://prozell-cluster.de/projekte/mikal/'
         },
         {
             Dateiname: 'trockenbeschichten',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'optiex',
             text: 'Optimierte Herstellungsverfahren für High-Load Elektroden auf Basis von Extrusionsprozessen ',
             quelle: 'https://prozell-cluster.de/projekte/optiex/'
         },
         {
             Dateiname: 'beschichten',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'beschichten_und_trocknen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'oekotrop_buerstenauftrag',
             text: 'Ökologisch schonende Trockenbeschichtung von Batterie- Elektroden mit optimierter Elektrodenstruktur',
             quelle: 'https://prozell-cluster.de/projekte/oekotrop/'
         },
         {
             Dateiname: 'highstructures_extrusion',
             text: 'Hierarchische Strukturierung hochkapazitiver Elektroden',
             quelle: 'https://prozell-cluster.de/projekte/histructures/'
         },
         {
             Dateiname: 'highstructures_laser',
             text: 'Hierarchische Strukturierung hochkapazitiver Elektroden',
             quelle: 'https://prozell-cluster.de/projekte/histructures/'
         },
         {
             Dateiname: 'epic',
             text: 'Erhöhung der Durchsatzgeschwindigkeit in der Elektrodenproduktion durch ein innovatives Trocknungsmanagement',
             quelle: 'https://prozell-cluster.de/projekte/epic/'
         },
         {
             Dateiname: 'rollbatt',
             text: 'Weiterentwicklung von Wickelprozessen und zylindrischen Zellen',
             quelle: 'https://prozell-cluster.de/projekte/rollbatt/'
         },
         {
             Dateiname: 'trocknen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'praelithiierung',
             text: 'Prälithiierung von Elektroden',
             quelle: ''
         },
         {
             Dateiname: 'kalandrieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'praeli_li_salz',
             text: 'Prälithiierung von Elektroden durch ein Bad in Li-Salz',
             quelle: 'https://prozell-cluster.de/projekte/praeli/'
         },
         {
             Dateiname: 'praeli_pvd',
             text: 'Prälithiierung von Elektroden im Physical Vapor Deposition Verfahren',
             quelle: 'https://prozell-cluster.de/projekte/praeli/'
         },
         {
             Dateiname: 'praeli_opferanode',
             text: 'Prälithiierung von Elektroden unter Einsatz von Opferanoden',
             quelle: 'https://prozell-cluster.de/projekte/praeli/'
         },
         {
             Dateiname: 'strukturierung',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'profistruk_strukturierung',
             text: 'Prozess- und Anlagenentwicklung zur prozessintegrierten Inline-Strukturierung von Lithium-Ionen-Elektroden',
             quelle: 'https://prozell-cluster.de/projekte/profistruk/'
         },
         {
             Dateiname: 'laengsschneiden',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'intensivtrocknen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'vereinzeln',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'holib_vereinzeln',
             text: 'Hochdurchsatzverfahren in der Fertigung von Lithium-Ionen-Batterien',
             quelle: 'https://prozell-cluster.de/projekte/holib/'
         },
         {
             Dateiname: 'laminieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'stapeln',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'e_qual',
             text: 'Datenbasierte Prozess- und Methodenentwicklung zur Effizienz- und Qualitätssteigerung in der Li-Ionen-Zellproduktion',
             quelle: 'https://prozell-cluster.de/projekte/e-qual/'
         },
         {
             Dateiname: 'holib_stapeln',
             text: 'Hochdurchsatzverfahren in der Fertigung von Lithium-Ionen-Batterien',
             quelle: 'https://prozell-cluster.de/projekte/holib/'
         },
         {
             Dateiname: 'z_falten',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'wickeln',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'kontaktieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'assemblieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'pouchbeutel_gehaeuse_verschliessen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'elektrolyt_dosieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'befuelloeffnung_verschliessen',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'cell_fill',
             text: 'Prozess-Struktur-Eigenschaftsbeziehung für Befüllungs- und Wettingprozesse von großformatigen Lithium-Ionen-Batterien',
             quelle: 'https://prozell-cluster.de/projekte/cell-fill/'
         },
         {
             Dateiname: 'formieren',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'formel',
             text: 'Optimierung und Funktionsintegration der Formierung und des End-of-Line Tests',
             quelle: 'https://prozell-cluster.de/projekte/formel/'
         },
         {
             Dateiname: 'reifelagern',
             text: '',
             quelle: ''
         },
         {
             Dateiname: 'pruefen_und_klassifizieren',
             text: '',
             quelle: ''
         },
     ] */

    return (

        <>
            {props.tooltips !== null &&
                JSON.parse(props.tooltips).map(item => item.Dateiname === props.quelle && item.text !== null &&
                    <Tooltip label="Close" width="200" key={item.Dateiname}>

                        <p style={{ fontWeight: "bold" }}>
                            {props.title}
                        </p>
                        <p>{item.text}</p>
                        <br />
                        {item.quelle !== null &&
                            <a rel="noreferrer" style={{ color: "white" }} href={item.quelle} target="_blank">mehr erfahren</a>}

                    </Tooltip>
                )}
        </>
    )
}

