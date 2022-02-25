import React, { useState, useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  zellchemie_state,
  zellchemie_name_state,
  empty_reducer,
  zellergebnisse_change
} from '../../../actions/index';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  Dropdown,
  Button,
} from 'carbon-components-react';
import Zellchemie_TableRow from './zellchemie_tablerow';
import MaterialInfoTable from './material_info_table';
import WeitereParameterTablerow from './weitere_parameter_tablerow';

export default function Zellchemie() {
  const dispatch = useDispatch();

  //redux states nur zum Test, können später raus
  //Zellmaße
  const zellformat = useSelector(state => state.zellformat);

  //redux states
  //Daten der aktuell ausgewählten Zellchemie
  const zellchemie = useSelector(state => state.zellchemie);
  //Name der aktuell ausgewählten Zellchemie
  const zellchemieName = useSelector(state => state.zellchemieName);
  //Infos zu den Materialien der aktuell ausgewählten Zellchemie
  const materialInfos = useSelector(state => state.empty);
  //Alle Materialien
  const materialien = useSelector(state => state.zellmaterialien);
  //Zellformat & Zellformatname für den Export
  const zellformatName = useSelector(state => state.zellformatName);
  //Ah pro Zelle und GWh/Jahr für die Fabrik separat gespeichert
  const GWH_Jahr_AH_Zelle = useSelector(state => state.GWH_Jahr_AH_Zelle)

  //Liste der aktuell auswählbaren Zellchemien
  const [currentZellchemien, setCurrentZellchemien] = useState(null);

  //ruft die Tabelle aller möglichen Zellchemien aus der Datenbank ab
  tabelle_abrufen('Zellchemien').then(result => setCurrentZellchemien(result));
  //ruft die Tabelle aller möglichen Materialien aus der Datenbank ab
  //tabelle_abrufen('materialien').then(result => setmaterialen(result));

  //Abrufen der Informationen zu einer bestimmten Zellchemie aus der Datenbank mithilfe der funtion "tabelle_abrufen"
  //"result" stellt die Tabelle dar, innerhalb des "then" kann damit gearbeitet werden
  function auswahl_zellchemie(event) {
    dispatch(zellchemie_name_state(event.selectedItem));
    var Dateiname = JSON.parse(currentZellchemien).filter(
      item => item.Beschreibung === event.selectedItem
    )[0].Dateiname;

    tabelle_abrufen(Dateiname).then(result =>
      dispatch(zellchemie_state(result))
    );
  }

  function fill_materials() {
    var listOfMaterials = JSON.parse(materialien).map(
      item => item.Beschreibung
    ); //Auflistung aller genutzten Materialien einer Kategorie, für die Filterung später
    var newState = [];
    var liste = [];

    JSON.parse(zellchemie)
      .filter(item =>
        listOfMaterials.includes(item.Beschreibung) ? true : false
      )
      .map(item => liste.push(item.Beschreibung));

    liste.map(item =>
      newState.push(
        tabelle_abrufen(material_Dateiname(item)).then(result => ({
          [item]: JSON.parse(result),
        }))
      )
    );

    Promise.all(newState).then(values => {
      dispatch(empty_reducer(values));
    });
  }

  //Erweiterung für fill_materials()
  //Wichtige Funktion! Die Funtkion arbeitet immer dann wenn Zellinfo sich ändert -> kann doppelten API Abruf durchführen
  //Funktion wird immer dann durchgeführt wenn such {Zellinfo} ändert (ausser beim ersten mal, dafür ist didMount da)
  //wenn Zellinfo = null muss auch didMount = false, verhindert das initiale rendern
  const didMount = useRef(false);
  useEffect(() => {
    didMount.current ? fill_materials() : (didMount.current = true);
  }, [zellchemie]);
  /*
  function setMountFalse() {
    didMount.current = false;
  }
  */

  //allgemeine Funktion die eine Tabelle aus der Datenbank abruft und als string zurück gibt
  async function tabelle_abrufen(tabelle_dateiname) {
    const res = await fetch('/tabelle_abrufen', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tabelle: tabelle_dateiname,
      }),
    });
    const data = await res.json();
    return data.tabelle;
  }

  //löscht einzelnes Material (ganzes Object) aus der aktuellen Zellchemie
  function delete_(Beschreibung_delete) {
    var newArray = [
      ...JSON.parse(zellchemie).filter(
        item => item.Beschreibung !== Beschreibung_delete
      ),
    ];
    dispatch(zellchemie_state(JSON.stringify(newArray)));
    material_entfernen(Beschreibung_delete);
  }

  //fügt einzelnes Material (ganzes Object) zu der aktuellen Zellchemie hinzu
  function add_(Beschreibung_add) {
    var newObject = JSON.parse(materialien).filter(
      item => item.Beschreibung === Beschreibung_add
    )[0];
    var newArray = [...JSON.parse(zellchemie), newObject];
    dispatch(zellchemie_state(JSON.stringify(newArray)));
    material_hinzufügen(Beschreibung_add);
  }

  //Ersetzt ein Material aus der aktuellen Zellchemie, gilt nur für "unique" Materialien
  function replace_(Beschreibung_replace) {
    var newObject = JSON.parse(materialien).filter(
      item => item.Beschreibung === Beschreibung_replace
    )[0];
    var newArray = [
      ...JSON.parse(zellchemie).filter(
        item => item.Kategorie !== newObject.Kategorie
      ),
      newObject,
    ];
    dispatch(zellchemie_state(JSON.stringify(newArray)));
  }

  //Anpassen der Prozentzahl im State unter Beibehaltung der Reihenfolge
  function Anteil_prozent(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(zellchemie).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(zellchemie)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    dispatch(zellchemie_state(JSON.stringify(newState)));
  }

  //Anpassen einzelner Werte der verwendeten Materialien im State, etwas komplizierter da der State verschachtelt ist
  function material_anpassen(Material, Beschreibung, neuerWert) {
    console.log(Material, Beschreibung, neuerWert);
    let newState = [...materialInfos]; //shallow copy of old state
    var prevIndex = newState.findIndex(
      item => Object.keys(item)[0] === Material
    ); //index im State für das zu Änderndn Object
    let newObject = { ...newState[prevIndex] }; //Kopie des Materials als Objec
    let innerIndex = newObject[Material].findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im neuen Objects für das zu Ändernden Wertes
    let innerObject = [...newObject[Material]]; //Kopie der Eigenschaften des Materials als Liste von Objects
    let innerinnerObject = { ...innerObject[innerIndex] }; //Kopie der betreffenden Spalte
    innerinnerObject.Wert = neuerWert; //Wert Überschreiben
    innerObject[innerIndex] = innerinnerObject; //Alle Spalten des Materials
    newObject[Material] = innerObject;
    newState[prevIndex] = newObject;
    dispatch(empty_reducer(newState));
  }

  //eintfernt ein Material aus dem nested State "materialInfos"
  function material_entfernen(Material) {
    let newState = [...materialInfos].filter(
      item => Object.keys(item)[0] !== Material
    );
    dispatch(empty_reducer(newState));
  }

  //gleicht den Namen eines Materials in der Materialtabelle ab und gibt den entsprechenden Dateinamen zurück
  function material_Dateiname(Material) {
    var Dateiname = JSON.parse(materialien).filter(
      item => item.Beschreibung === Material
    )[0].Dateiname;
    return Dateiname;
  }

  //fügt Material zum nested State "materialInfos" hinzu
  async function material_hinzufügen(Material) {
    var Dateiname = JSON.parse(materialien).filter(
      item => item.Beschreibung === Material
    )[0].Dateiname;
    tabelle_abrufen(Dateiname).then(result =>
      dispatch(
        empty_reducer([...materialInfos, { [Material]: JSON.parse(result) }])
      )
    );
  }

  //schickt alle Zellinformationen an das Backend und ruft ein Ergebnis ab
  function Zell_ergebnis() {
    fetch('/Zellergebnisse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zellchemie: zellchemie,
        Materialinfos: JSON.stringify(materialInfos),
        zellformat: zellformat,
        zellformatName: JSON.stringify(zellformatName),
        GWh_Jahr_Ah_Zelle: JSON.stringify(GWH_Jahr_AH_Zelle)
      }),
    })
      .then(res => res.json())
      .then(data => {
        dispatch(zellergebnisse_change(data.Zellergebnisse));
      });
  }

  const props = {
    Zellchemie_TableRow_nicht_unique_Anteil: {
      Anteil: true,
      materialien: materialien,
      Zellchemie: zellchemie,
      onIncrement: Anteil_prozent,
      onChange: add_,
      onClick: delete_,
      unique: false,
    },
    Zellchemie_TableRow_unique_Anteil: {
      Anteil: true,
      materialien: materialien,
      Zellchemie: zellchemie,
      onIncrement: Anteil_prozent,
      onChange: replace_,
      onClick: delete_,
      unique: true,
    },
    Zellchemie_TableRow_unique_kein_Anteil: {
      Anteil: false,
      materialien: materialien,
      Zellchemie: zellchemie,
      onChange: replace_,
      onClick: delete_,
      unique: true,
    },
  };

  //var summe = 0
  //JSON.parse(zellchemie).filter(item => item)

  return (
    <div key="d">
      {currentZellchemien !== null && (
        <div key="a" style={{ width: 400 }}>
          <Dropdown
            className="zellformate__dropdown"
            id="default"
            //titleText="Zelltypen"
            helperText="This is some helper text"
            label="Dropdown menu options"
            items={JSON.parse(currentZellchemien).map(
              item => item.Beschreibung
            )}
            onChange={event => auswahl_zellchemie(event)}
          />
          {//Prüfung ob alle Vorraussetzungen für die Ergebnisse gegeben sind
          zellchemie !== null &&
          <Button onClick={() => Zell_ergebnis()}>Ergebnisse</Button>
          }
        </div>
      )}

      {zellchemie !== null && (
        <div key="c">
          <h3>{zellchemieName}</h3>
          
            {//Summenprüfung der Kathodenmaterialien
            JSON.parse(zellchemie)
              .filter(item=> item.Kategorie === "Aktivmaterial Kathode" || item.Kategorie === "Additive Kathode")
              .reduce((a,v) =>  a = a + v.Wert , 0 ) !== 100 &&
              <p style={{color: "red"}}>Summe der Kathodenmaterialien prüfen (
                {JSON.parse(zellchemie)
                .filter(item=> item.Kategorie === "Aktivmaterial Kathode" || item.Kategorie === "Additive Kathode")
                .reduce((a,v) =>  a = a + v.Wert , 0 )}
                %)</p>
              }
            {//Summenprüfung der Anodenmaterialien
            JSON.parse(zellchemie)
              .filter(item=> item.Kategorie === "Aktivmaterial Anode" || item.Kategorie === "Additive Anode")
              .reduce((a,v) =>  a = a + v.Wert , 0 ) !== 100 &&
              <p style={{color: "red"}}>Summe der Anodenmaterialien prüfen (
                {JSON.parse(zellchemie)
              .filter(item=> item.Kategorie === "Aktivmaterial Anode" || item.Kategorie === "Additive Anode")
              .reduce((a,v) =>  a = a + v.Wert , 0 )}
              %)</p>
              }

          <Table useZebraStyles size="compact" className="zellchemie_table">
            <TableHead>
              <TableRow>
                <TableHeader style={{ backgroundColor: 'white' }}>
                </TableHeader>
                <TableHeader style={{ backgroundColor: 'white' }}>
                <h3>Zusammensetzung</h3>
                </TableHeader>
                <TableHeader style={{ backgroundColor: 'white' }}>
                </TableHeader>
                <TableHeader style={{ backgroundColor: 'white' }}>
                </TableHeader>
              </TableRow>
            </TableHead>

            <TableHead key="b">
              <TableRow>
                <TableHeader style={{ backgroundColor: 'white' }} />
                <TableHeader>
                  <p>Beschreibung</p>
                </TableHeader>
                <TableHeader>
                  <p>Anteil [%]</p>
                </TableHeader>
                <TableHeader>
                  <p>Materialien</p>
                </TableHeader>
              </TableRow>
            </TableHead>
            {materialien !== null && (
              <>
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_Anteil}
                  filter="Aktivmaterial Kathode"
                />
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_nicht_unique_Anteil}
                  filter="Additive Kathode"
                />
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_nicht_unique_Anteil}
                  filter="Lösemittel Kathode"
                />
                <Zellchemie_TableRow
                  filter="Kollektorfolie Kathode"
                  {...props.Zellchemie_TableRow_unique_kein_Anteil}
                />
                {/* Parameter Anode */}
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_Anteil}
                  filter="Aktivmaterial Anode"
                />
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_nicht_unique_Anteil}
                  filter="Additive Anode"
                />
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_nicht_unique_Anteil}
                  filter="Lösemittel Anode"
                />
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_kein_Anteil}
                  filter="Kollektorfolie Anode"
                />
                {/* Parameter Separator */}
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_kein_Anteil}
                  filter="Separator"
                />
                {/* Parameter Elekotrlyt */}
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_kein_Anteil}
                  filter="Elektrolyt"
                />
                {/* Parameter Hülle */}
                <Zellchemie_TableRow
                  {...props.Zellchemie_TableRow_unique_kein_Anteil}
                  filter="Hülle"
                />
              </>
            )}
          </Table>
          <h2>Weitere Parameter</h2>
          <Table useZebraStyles size="compact" className="zellchemie_table">
            <TableHead>
              <TableRow>
                <TableHeader>
                  <p>Beschreibung</p>
                </TableHeader>
                <TableHeader>
                  <p>Wert</p>
                </TableHeader>
                <TableHeader>
                  <p>Einheit</p>
                </TableHeader>
              </TableRow>
            </TableHead>

            <WeitereParameterTablerow
              onChange={Anteil_prozent}
              Zellchemie={zellchemie}
              filter="Allgemeine Parameter"
            />
            <WeitereParameterTablerow
              onChange={Anteil_prozent}
              Zellchemie={zellchemie}
              filter="Elektrodenparameter Kathode"
            />
            <WeitereParameterTablerow
              onChange={Anteil_prozent}
              Zellchemie={zellchemie}
              filter="Elektrodenparameter Anode"
            />
          </Table>
        </div>
      )}

      {/* Darstellung der verschiedenen Materialien aus "materialinfors" mit der Möglichkeit, die Werte anzupassen
{JSON.parse(zellchemie).map(item=>console.log(item.Beschreibung))}
*/}

      <h2>Materialien Details</h2>
      {/*{materialInfos.length !== 0 &&*/}
      {materialInfos !== null &&
        materialInfos.map(item => (
          <MaterialInfoTable
            key={Object.keys(item)[0]}
            header={Object.keys(item)[0]}
            content={item[Object.keys(item)[0]]}
            onChange={material_anpassen}
          />
        ))}
    </div>
  );
}
