import React, { useState, useEffect, useRef } from 'react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  Dropdown,
  TableBody,
  TableCell,
  NumberInput,
  Tabs,
  Tab,
  Button,
  ContentSwitcher,
  Switch,
} from 'carbon-components-react';
import Zellchemie_TableRow from './zellchemie_tablerow';
import MaterialInfoTable from './material_info_table';

export default function Zellchemie() {
  //Liste der aktuell auswählbaren Materiealien
  const [materialien, setmaterialen] = useState(null);

  //Liste der aktuell auswählbaren Zellchemien
  const [currentZellchemien, setCurrentZellchemien] = useState(null);

  //Aktuell ausgewählte Zellchemie
  const [currentZellchemie, setCurrentZellchemie] = useState(null);

  //Aktuell ausgewählte Zellchemie
  const [currentZellchemieTitle, setCurrentZellchemieTitle] = useState(null);

  //Informationen zu den ausgewählten Bestandteilen, ein State mit mehreren Tables, jeweils gespeichert direkt als JSON Format
  const [materialInfos, setMaterialInfos] = useState([]);

  //ruft die Tabelle aller möglichen Zellchemien aus der Datenbank ab
  tabelle_abrufen('Zellchemien').then(result => setCurrentZellchemien(result));
  //ruft die Tabelle aller möglichen Materialien aus der Datenbank ab
  tabelle_abrufen('materialien').then(result => setmaterialen(result));

  //Abrufen der Informationen zu einer bestimmten Zellchemie aus der Datenbank mithilfe der funtion "tabelle_abrufen"
  //"result" stellt die Tabelle dar, innerhalb des "then" kann damit gearbeitet werden
  function auswahl_zellchemie(event) {
    setCurrentZellchemieTitle(event.selectedItem);
    var Dateiname = JSON.parse(currentZellchemien).filter(
      item => item.Beschreibung === event.selectedItem
    )[0].Dateiname;

    tabelle_abrufen(Dateiname).then(result => setCurrentZellchemie(result));
    /*
    & 
    (JSON.parse(result)
    .filter(item => listOfMaterials.includes(item.Beschreibung) ? true:false)
    .map(item=> liste.push(item.Beschreibung))));
    
    var liste2 = ["NCM 622", "Graphit", "A-Binder 2", "A-Binder 1"]

    liste2.map(item=> newState.push(tabelle_abrufen(material_Dateiname(item)).then(result => ({[item]:JSON.parse(result)}))))
    console.log(newState)
    Promise.all(newState).then((values) => {
      setMaterialInfos(values)
      */
  }

  function fill_materials() {
    var listOfMaterials = JSON.parse(materialien).map(
      item => item.Beschreibung
    ); //Auflistung aller genutzten Materialien einer Kategorie, für die Filterung später
    var newState = [];
    var liste = [];

    JSON.parse(currentZellchemie)
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
    liste.map(item => console.log(item));
    console.log(newState);

    Promise.all(newState).then(values => {
      setMaterialInfos(values);
    });
  }

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
      ...JSON.parse(currentZellchemie).filter(
        item => item.Beschreibung !== Beschreibung_delete
      ),
    ];
    setCurrentZellchemie(JSON.stringify(newArray));
    material_entfernen(Beschreibung_delete);
  }

  //fügt einzelnes Material (ganzes Object) zu der aktuellen Zellchemie hinzu
  function add_(Beschreibung_add) {
    var newObject = JSON.parse(materialien).filter(
      item => item.Beschreibung === Beschreibung_add
    )[0];
    var newArray = [...JSON.parse(currentZellchemie), newObject];
    setCurrentZellchemie(JSON.stringify(newArray));
    material_hinzufügen(Beschreibung_add);
  }

  //Ersetzt ein Material aus der aktuellen Zellchemie, gilt nur für "unique" Materialien
  function replace_(Beschreibung_replace) {
    var newObject = JSON.parse(materialien).filter(
      item => item.Beschreibung === Beschreibung_replace
    )[0];
    var newArray = [
      ...JSON.parse(currentZellchemie).filter(
        item => item.Kategorie !== newObject.Kategorie
      ),
      newObject,
    ];
    setCurrentZellchemie(JSON.stringify(newArray));
  }

  //Anpassen der Prozentzahl im State unter Beibehaltung der Reihenfolge
  function Anteil_prozent(Beschreibung, neuerWert) {
    var prevIndex = JSON.parse(currentZellchemie).findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im State für das zu Ändernde Object
    let newState = [...JSON.parse(currentZellchemie)]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    newObject.Wert = neuerWert; //Prozentzahl anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    setCurrentZellchemie(JSON.stringify(newState));
  }

  //Anpassen einzelner Werte der verwendeten Materialien im State, etwas komplizierter da der State verschachtelt ist
  function material_anpassen(Material, Beschreibung, neuerWert) {
    var prevIndex = materialInfos.findIndex(
      item => Object.keys(item)[0] === Material
    ); //index im State für das zu Änderndn Object
    let newState = [...materialInfos]; //shallow copy of old state
    let newObject = { ...newState[prevIndex] }; //shallow copy of specific Object
    let innderIndex = newObject[Material].findIndex(
      item => item.Beschreibung === Beschreibung
    ); //index im neuen Objects für das zu Ändernden Wertes
    newObject[Material][innderIndex].Wert = neuerWert; //Wert anpassen
    newState[prevIndex] = newObject; //unter dem gleichen Index im neuen State überschreiben
    setMaterialInfos(newState);
  }

  function material_entfernen(Material) {
    let newState = [...materialInfos].filter(
      item => Object.keys(item)[0] !== Material
    );
    setMaterialInfos(newState);
  }

  function material_Dateiname(Material) {
    var Dateiname = JSON.parse(materialien).filter(
      item => item.Beschreibung === Material
    )[0].Dateiname;
    return Dateiname;
  }

  async function material_hinzufügen(Material) {
    var Dateiname = JSON.parse(materialien).filter(
      item => item.Beschreibung === Material
    )[0].Dateiname;
    tabelle_abrufen(Dateiname).then(result =>
      setMaterialInfos([...materialInfos, { [Material]: JSON.parse(result) }])
    );
  }

  //schickt alle Zellinformationen an das Backend und ruft ein Ergebnis ab
  function Zell_ergebnis() {
    fetch('/Zellergebnisse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zellchemie: currentZellchemie,
        Materialinfos: JSON.stringify(materialInfos),
      }),
    })
      .then(res => res.json())
      .then(data => {
        console.log(data.Zellinfo);
      });
  }

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
          <Button onClick={() => fill_materials()}>Daten</Button>
          <Button onClick={() => Zell_ergebnis()}>Ergebnisse</Button>
        </div>
      )}

      {currentZellchemie !== null && (
        <div key="c">
          <h3>{currentZellchemieTitle}</h3>
          <h2>Materialien</h2>
          <Table useZebraStyles size="compact" className="zellchemie_table">
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
            {/* Parameter Kathode */}
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Aktivmaterial Kathode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Additive Kathode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Lösemittel Kathode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Kollektorfolie Kathode"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            {/* Parameter Anode */}
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Aktivmaterial Anode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Additive Anode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Lösemittel Anode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Kollektorfolie Anode"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            {/* Parameter Separator */}
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Separator"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            {/* Parameter Elekotrlyt */}
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Elektrolyt"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
            {/* Parameter Hülle */}
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Hülle"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              //onAdd={material_hinzufügen}
              unique={true}
            />
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
            <TableBody>
              <TableRow>
                <TableCell>
                  <h4>
                    <u>Allgenmeine Parameter</u>
                  </h4>
                </TableCell>
                <TableCell />
                <TableCell />
              </TableRow>
              {JSON.parse(currentZellchemie)
                .filter(item => item.Kategorie === 'Allgemeine Parameter')
                .map(item => (
                  <TableRow>
                    <TableCell>{item.Beschreibung}</TableCell>
                    <TableCell key={item.id}>
                      <NumberInput
                        size="sm"
                        min={0}
                        id="carbon-number"
                        invalidText="Ungültiger Wert"
                        value={item.Wert}
                        onChange={e =>
                          Anteil_prozent(
                            item.Beschreibung,
                            e.imaginaryTarget.value
                          )
                        }
                      />
                    </TableCell>
                    <TableCell>{item.Einheit}</TableCell>
                  </TableRow>
                ))}

              <TableRow>
                <TableCell>
                  <h4>
                    <u>Elektrodenparameter Kathode</u>
                  </h4>
                </TableCell>
                <TableCell />
                <TableCell />
              </TableRow>
              {JSON.parse(currentZellchemie)
                .filter(
                  item => item.Kategorie === 'Elektrodenparameter Kathode'
                )
                .map(item => (
                  <TableRow>
                    <TableCell>{item.Beschreibung}</TableCell>
                    <TableCell key={item.id}>
                      <NumberInput
                        size="sm"
                        min={0}
                        id="carbon-number"
                        invalidText="Ungültiger Wert"
                        value={item.Wert}
                        onChange={e =>
                          Anteil_prozent(
                            item.Beschreibung,
                            e.imaginaryTarget.value
                          )
                        }
                      />
                    </TableCell>
                    <TableCell>{item.Einheit}</TableCell>
                  </TableRow>
                ))}

              <TableRow>
                <TableCell>
                  <h4>
                    <u>Elektrodenparameter Anode</u>
                  </h4>
                </TableCell>
                <TableCell />
                <TableCell />
              </TableRow>
              {JSON.parse(currentZellchemie)
                .filter(item => item.Kategorie === 'Elektrodenparameter Anode')
                .map(item => (
                  <TableRow>
                    <TableCell>{item.Beschreibung}</TableCell>
                    <TableCell key={item.id}>
                      <NumberInput
                        size="sm"
                        min={0}
                        id="carbon-number"
                        invalidText="Ungültiger Wert"
                        value={item.Wert}
                        onChange={e =>
                          Anteil_prozent(
                            item.Beschreibung,
                            e.imaginaryTarget.value
                          )
                        }
                      />
                    </TableCell>
                    <TableCell>{item.Einheit}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Darstellung der verschiedenen Materialien aus "materialinfors" mit der Möglichkeit, die Werte anzupassen
{JSON.parse(currentZellchemie).map(item=>console.log(item.Beschreibung))}
*/}

      <h2>Materialien Details</h2>

      {materialInfos.length !== 0 &&
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
