import React, { useState, useEffect, useRef } from 'react';
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
  /*
    useEffect(() => {
      fetch('/Zellchemien')
        .then(res => res.json())
        .then(data => {
          setCurrentZellchemien(data.Zellchemien);
        });
    }, []);
    */

  //ruft die Tabelle aller möglichen Materialien aus der Datenbank ab
  tabelle_abrufen('materialien').then(result => setmaterialen(result));
  /*
  useEffect(() => {
    fetch('/Zellmaterialien')
      .then(res => res.json())
      .then(data => {
        setmaterialen(data.Zellmaterialien);
      });
  }, []);
*/

  //Abrufen der Informationen zu einer bestimmten Zellchemie aus der Datenbank
  /*
  function auswahl_zellchemie(event){
    setCurrentZellchemieTitle(event.selectedItem)
    var Dateiname = JSON.parse(currentZellchemien).filter(item => item.Beschreibung === event.selectedItem)[0].Dateiname
    fetch('/Zellchemiewahl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zellchemiewahl: Dateiname,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setCurrentZellchemie(data.Zellchemie);
        console.log(JSON.parse(currentZellchemie));
      });
  }
  */

  //Abrufen der Informationen zu einer bestimmten Zellchemie aus der Datenbank mithilfe der funtion "tabelle_abrufen"
  //"result" stellt die Tabelle dar, innerhalb des "then" kann damit gearbeitet werden
  function auswahl_zellchemie(event) {
    setCurrentZellchemieTitle(event.selectedItem);
    var Dateiname = JSON.parse(currentZellchemien).filter(
      item => item.Beschreibung === event.selectedItem
    )[0].Dateiname;
    tabelle_abrufen(Dateiname).then(result => setCurrentZellchemie(result));
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
  }

  //fügt einzelnes Material (ganzes Object) zu der aktuellen Zellchemie hinzu
  function add_(Beschreibung_add) {
    var newObject = JSON.parse(materialien).filter(
      item => item.Beschreibung === Beschreibung_add
    )[0];
    var newArray = [...JSON.parse(currentZellchemie), newObject];
    setCurrentZellchemie(JSON.stringify(newArray));
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
    newObject.Anteil = neuerWert; //Prozentzahl anpassen
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
    console.log(currentZellchemie);
    console.log(JSON.stringify(materialInfos));
  }

  function material_entfernen(Material) {
    let newState = [...materialInfos].filter(
      item => Object.keys(item)[0] !== Material
    );
    setMaterialInfos(newState);
  }

  return (
    <div>
      {currentZellchemien == null ? (
        <p />
      ) : (
        <div style={{ width: 400 }}>
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
          {/* 
            <Button onClick={()=>
              tabelle_abrufen("NCM_622").then(result => setMaterialInfos([...materialInfos,{"NCM 622":JSON.parse(result)}]))
            }>NCM 622</Button>
            <Button onClick={()=>
              tabelle_abrufen("graphit").then(result => setMaterialInfos([...materialInfos,{"Graphit":JSON.parse(result)}])) 
            }>Graphipt</Button>
            <Button onClick={()=>
              console.log(materialInfos)
            }>Klick me 3</Button>
            <Button kind="danger" onClick={()=>
              material_entfernen("NCM 622")
            }>remove NCM</Button>
          */}
        </div>
      )}

      {currentZellchemie == null ? (
        <p />
      ) : (
        <div>
          <h3>{currentZellchemieTitle}</h3>
          <Table useZebraStyles size="compact" className="zellchemie_table">
            <TableHead>
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
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Aktivmaterial Kathode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={replace_}
              onClick={delete_}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Zusatzmaterial Kathode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Aktivmaterial Anode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={replace_}
              onClick={delete_}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={true}
              materialien={materialien}
              filter="Zusatzmaterial Anode"
              Zellchemie={currentZellchemie}
              onIncrement={Anteil_prozent}
              onChange={add_}
              onClick={delete_}
              unique={false}
            />
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Kollektorfolie Kathode"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Kollektorfolie Anode"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              unique={true}
            />
            <Zellchemie_TableRow
              Anteil={false}
              materialien={materialien}
              filter="Elektrolyt"
              Zellchemie={currentZellchemie}
              onChange={replace_}
              onClick={delete_}
              unique={true}
            />
          </Table>
        </div>
      )}

      {materialInfos.length == 0 ? (
        <p />
      ) : (
        materialInfos.map(item => (
          <MaterialInfoTable
            header={Object.keys(item)[0]}
            content={item[Object.keys(item)[0]]}
            onChange={material_anpassen}
          />
        ))
      )}
    </div>
  );
}
