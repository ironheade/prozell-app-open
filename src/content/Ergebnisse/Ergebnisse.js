import React, { useState } from 'react';
import { Accordion, AccordionItem, Breadcrumb, BreadcrumbItem, Button } from 'carbon-components-react';
import { useSelector, useDispatch } from 'react-redux'
import DfTable from './components/table_from_df'
import MyStackedBarChart from './components/bar_graph'
import GesamtkostenDonut from './components/GesamtkostenDonut';
import Alluvial from './components/AlluvialChart';
import { ergebnisTabelle_change } from '../../actions'
import SimpleTable from './components/simple_table';
import SimpleTableNested from './components/simple_table_nested'
import SimpleTableProzessroute from './components/simple_table_prozessroute'
import DownloadButton from './components/DownloadButton';
import Treemap from './components/Treemap';



export default function Ergebnisse() {
  const dispatch = useDispatch();
  //Ergebnisse der Zellberechnung
  const Zellergebnisse = useSelector(state => state.zellergebnisse)
  //aktuelle Prozessroute
  const prozessRoute = useSelector(state => state.prozessRoute)
  //Daten zur aktuellen Prozessroute
  const prozessschrittDaten = useSelector(state => state.prozessschrittDaten)
  //Infos zu den Materialien der aktuell ausgewählten Zellchemie
  const materialInfos = useSelector(state => state.empty);
  //Infos zur aktuell ausgewählten Zellchemie
  const zellchemie = useSelector(state => state.zellchemie);

  const oekonomischeParameter = useSelector(state => state.oekonomischeParameter);
  const mitarbeiterLogistik = useSelector(state => state.mitarbeiterLogistik);
  const gebaeude = useSelector(state => state.gebaeude);
  const rueckgewinnung = useSelector(state => state.rueckgewinnung);

  //const [ergebnissTabelle, setErgebnissTabelle] = useState(null)
  const ergebnisTabelle = useSelector(state => state.ergebnisTabelle)
  const [materialkosten, setMaterialkosten] = useState(null)
  const [materialverlust, setMaterialverlust] = useState(null)
  const [baukosten, setBaukosten] = useState(null)
  const [flaechenverteilung, setFlaechenverteilung] = useState(null)



  const [hintergrundDatenHidden, setHintergrundDatenHidden] = useState(true)

  //schickt alle Informationen an das Backend und ruft ein Ergebnis ab
  function Ergebnis() {
    fetch('/Ergebnisse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zellergebnisse: Zellergebnisse,
        Zellchemie: zellchemie,
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
        dispatch(ergebnisTabelle_change(data.Ergebnisse));
        setMaterialkosten(JSON.parse(data.Materialkosten));
        setMaterialverlust(JSON.parse(data.Rückgewinnung));
        setBaukosten(JSON.parse(data.Baukosten));
        setFlaechenverteilung(JSON.parse(data.Flächenverteilung))
      });
    setHintergrundDatenHidden(false)
  }

  //Erstellt einen Array mit den Prozessschritten in der richtigen Reihenfolge
  function create_ProzessschrittArray() {
    var newArray = []
    prozessRoute.map(item => item[Object.keys(item)[0]].map(inner_item => //liste mit den Prozessschritten pro Abschnitt
      newArray.push(inner_item))) //jeweils die Dateinamen
    return (newArray)

  }

  const Kostenfaktoren = [
    "Materialkosten",
    'Personalkosten',
    'Energiekosten',
    'Instandhaltungskosten',
    'Flächenkosten',
    'Kalkulatorische Zinsen',
    'Ökonomische Abschreibung'
  ]


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

      {
        prozessschrittDaten !== null && Zellergebnisse !== null
        &&
        <Button onClick={Ergebnis}>Ergebnisse</Button>
      }
      

      {Zellergebnisse === null && <h3>Zellberechnung nicht vollständig</h3>}
      {prozessschrittDaten === null && <h3>Prozessroute nicht vollständig</h3>}

      {ergebnisTabelle !== null && materialkosten !== null && baukosten !== null &&
        <>

          <h1>Produktionskosten</h1>
          <p style={{ "backgroundColor": "#feedf4", "width": "200px" }}> Trockenraum rot markiert</p>
          <MyStackedBarChart data={ergebnisTabelle} Kostenfaktoren={Kostenfaktoren} Prozessroute={create_ProzessschrittArray()} />
          <div style={{
            display: "flex",
            flexDirection: "row"
          }}>
            <h3>Ergebnistabelle</h3>
            <DownloadButton name="Ergebnistabelle" data={ergebnisTabelle} />
          </div>
          <DfTable data={ergebnisTabelle} />

          <div style={{ "height": "100px" }}></div>
          <h1>Kostenfluss</h1>
          <Alluvial data={materialverlust} data_kosten={materialkosten} rueckgewinnung={rueckgewinnung} />
          <div style={{ "height": "100px" }}></div>
          <h1>Gesamtkosten Jahresproduktion</h1>
          <GesamtkostenDonut 
            data_kosten={materialkosten}
            data={ergebnisTabelle}
            Kostenfaktoren={Kostenfaktoren}
            baukosten={baukosten} />

          {flaechenverteilung !== null && <Treemap data={flaechenverteilung}/>}
        </>
        
      }
      <Accordion hidden={hintergrundDatenHidden}>
        <AccordionItem title="Hintergrunddaten">
          <div id="ErgebnisAccordion">

            <div className='subdiv'>
              {Zellergebnisse !== null &&
                <SimpleTable name="Zellergebnisse" data={Zellergebnisse} />}
            </div>

            <div className='subdiv'>
              {prozessRoute !== null &&
                <SimpleTableProzessroute data={prozessRoute} />}
            </div>

            <div className='subdiv'>
              {zellchemie !== null &&
                <SimpleTable name="Zellchemie" data={zellchemie} />}
            </div>

            <div className='subdiv'>
              {prozessschrittDaten !== null &&
                <SimpleTableNested name="Prozessdetails" data={prozessschrittDaten} />}
            </div>

            <div className='subdiv'>
              {materialInfos !== null &&
                <SimpleTableNested name="Materialinfos" data={materialInfos} />}
            </div>

            <div className='subdiv'>
              {oekonomischeParameter !== null &&
                <SimpleTable name="Ökonomische Parameter" data={oekonomischeParameter} />}
            </div>

            <div className='subdiv'>
              {mitarbeiterLogistik !== null &&
                <SimpleTable name="Mitarbeiter und Logistik" data={mitarbeiterLogistik} />}
            </div>

            <div className='subdiv'>
              {gebaeude !== null &&
                <SimpleTable name="Gebäude" data={gebaeude} />}
            </div>

            <div className='subdiv'>
              {rueckgewinnung !== null &&
                <SimpleTable name="Rückgewinnung" data={rueckgewinnung} />}
            </div>

          </div>
        </AccordionItem>

        <AccordionItem title="Hintergrunddaten JSON Format">
          <h1>Zellergebnisse</h1>
          {Zellergebnisse !== null &&
            <p>{Zellergebnisse}</p>}

          <h1>Prozessroute</h1>
          {prozessRoute !== null &&
            <p>{JSON.stringify(prozessRoute)}</p>}

          <h1>Zellchemie</h1>
          {zellchemie !== null &&
            <p>{zellchemie}</p>}

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

          <h1>Rückgewinnung</h1>
          {rueckgewinnung !== null &&
            <p>{rueckgewinnung}</p>}

          <h1>Ergebnisse</h1>
          {ergebnisTabelle !== null &&
            <p>{ergebnisTabelle}</p>}
        </AccordionItem>

      </Accordion>

    </div>
  );
}
