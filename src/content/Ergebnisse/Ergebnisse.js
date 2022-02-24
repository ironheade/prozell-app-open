import React, { useState } from 'react';
import { Breadcrumb, BreadcrumbItem, Button } from 'carbon-components-react';
import { useSelector } from 'react-redux'
import {
  TableRow,
  TableCell,
  TableBody,
  Table,
  TableHead,
  TableHeader,
} from 'carbon-components-react';
import DfTable from './table_from_df'

export default function Ergebnisse() {

  //Ergebnisse der Zellberechnung
  const Zellergebnisse = useSelector(state => state.zellergebnisse)
  //aktuelle Prozessroute
  const prozessRoute = useSelector(state => state.prozessRoute)
  //Daten zur aktuellen Prozessroute
  const prozessschrittDaten = useSelector(state => state.prozessschrittDaten)
  //Infos zu den Materialien der aktuell ausgewählten Zellchemie
  const materialInfos = useSelector(state => state.empty);
  
  const oekonomischeParameter = useSelector(state => state.oekonomischeParameter);
  const mitarbeiterLogistik = useSelector(state => state.mitarbeiterLogistik);
  const gebaeude = useSelector(state => state.gebaeude);

  const [ergebnissTabelle, setErgebnissTabelle] = useState(null)

  

  //schickt alle Informationen an das Backend und ruft ein Ergebnis ab
  function Ergebnis() {
    fetch('/Ergebnisse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zellergebnisse: Zellergebnisse,
        Prozessroute: JSON.stringify(prozessRoute),
        Prozessroute_array: create_ProzessschrittArray(),
        Prozessdetails: JSON.stringify(prozessschrittDaten),
        Materialinfos: JSON.stringify(materialInfos),
        Oekonomische_parameter: oekonomischeParameter,
        Mitarbeiter_Logistik: mitarbeiterLogistik,
        Gebaeude: gebaeude,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setErgebnissTabelle(data.Ergebnisse);
      });
    }

    //Erstellt einen Array mit den Prozessschritten in der richtigen Reihenfolge
    function create_ProzessschrittArray() {
      var newArray = []
      prozessRoute.map(item => item[Object.keys(item)[0]].map(inner_item => //liste mit den Prozessschritten pro Abschnitt
        newArray.push(inner_item))) //jeweils die Dateinamen
      return(newArray)

      }


  return (
    <div className="bx--grid bx--grid--full-width ergebnisse">
      <div className="bx--row __banner">
        <div className="bx--col-lg-16">
          <Breadcrumb noTrailingSlash aria-label="Page navigation">
            <BreadcrumbItem>
              <a href="/">Startseite</a>
            </BreadcrumbItem>
            <BreadcrumbItem>
              <a href="/#/Ergebnisse">Ergebnisse</a>
            </BreadcrumbItem>
          </Breadcrumb>
          <h1 className="__heading">Ergebnisse</h1>
        </div>
      </div>
      <Button onClick={Ergebnis}>Ergebnisse</Button>
      
      {ergebnissTabelle !== null &&
      <DfTable data={ergebnissTabelle}/>
      }

      <h1>Zellergebnisse</h1>
      {Zellergebnisse !== null &&
      <p>{Zellergebnisse}</p>}

      <h1>Prozessroute</h1>
      {prozessRoute !== null &&
      <p>{JSON.stringify(prozessRoute)}</p>}

      <h1>Prozessdetails</h1>
      {prozessschrittDaten !== null &&
      <p>{JSON.stringify(prozessschrittDaten)}</p>}

      <h1>Materialinfos</h1>
      {materialInfos !== null &&
      <p>{JSON.stringify(materialInfos)}</p>}

      <h1>Ökonomische Parameter</h1>
      {oekonomischeParameter !== null &&
      <p>{oekonomischeParameter}</p>}

      <h1>Mitarbeiter und Logistik</h1>
      {mitarbeiterLogistik !== null &&
      <p>{mitarbeiterLogistik}</p>}

      <h1>Gebäude</h1>
      {gebaeude !== null &&
      <p>{gebaeude}</p>}

    </div>
  );
}
