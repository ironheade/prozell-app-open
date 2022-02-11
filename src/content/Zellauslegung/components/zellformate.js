import React, { useState, useEffect, useRef } from 'react';
import { Dropdown } from 'carbon-components-react';
import { useSelector, useDispatch } from 'react-redux';
import {
  zellformat_change,
  zellformat_name_state,
} from '../../../actions/index';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  NumberInput,
} from 'carbon-components-react';
//import './../_zellauslegung.scss'

export default function Zellformate() {
  const dispatch = useDispatch();
  //Infos zur aktuell ausgewählten Zelle (Maße, etc.)
  const zellformat = useSelector(state => state.zellformat);
  //Name des aktuell ausgewähltes Zellformates
  const zellformatName = useSelector(state => state.zellformatName);
  //alle Zellformate
  const currentCells = useSelector(state => state.alleZellen);

  //Liste der aktuell auswählbaren Zellen
  //const [currentCells, setCurrentCells] = useState(null);
  //Liste aller Möglichen Zellformate
  const [currentZellformate, setCurrentZellformate] = useState('Pouchzelle');
  //Infos zur aktuell ausgewählten Zelle (Maße, etc.)
  const [Zellinfo, setZellinfo] = useState(null);
  //Aktuell ausgewähltes Zellformat
  const [currentZellformat, setCurrentZellformat] = useState(null);

  //ruft die Tabelle aller möglichen Zelltypen aus der Datenbank ab
  /*
  useEffect(() => {
    fetch('/Zellformate')
      .then(res => res.json())
      .then(data => {
        setCurrentCells(data.Zellformate);
      });
  }, []);
  */

  /*
  //Wichtige Funktion! Die Funtkion arbeitet immer dann wenn Zellinfo sich ändert -> kann doppelten API Abruf durchführen
  //Funktion wird immer dann durchgeführt wenn such {Zellinfo} ändert (ausser beim ersten mal, dafür ist didMount da)
  //wenn Zellinfo = null muss auch didMount = false, verhindert das initiale rendern 
  const didMount = useRef(false);
  useEffect(() => {
    didMount.current ?
      (JSON.parse(Zellinfo).map(item=> console.log(item)))
    :
      didMount.current = true;
    
  }, [Zellinfo]);
  function setMountFalse(){
    didMount.current = false;
  }
*/

  //ruft nach Auswahl der Zelle die Informationen zur Zelle aus der Datenbank ab
  const Zell_handler = event => {
    const value = event.target.value;
    //dispatch(zellformat_change(value))
    dispatch(
      zellformat_name_state(
        JSON.parse(currentCells).filter(item => item.Dateiname == value)[0]
          .Beschreibung
      )
    );

    fetch('/Zellwahl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zelle: value,
      }),
    })
      .then(res => res.json())
      .then(data =>
        //setZellinfo(data.Zellinfo)
        dispatch(zellformat_change(data.Zellinfo))
      );
  };

  //aktualisiert den state zur aktuell ausgewählten Zelle
  function handleChange(Beschreibung, neuerWert) {
    const newArr = JSON.parse(zellformat).map(item => {
      if (item.Beschreibung === Beschreibung) {
        return { ...item, Wert: neuerWert };
      }
      return item;
    });
    //setZellinfo(JSON.stringify(newArr));
    dispatch(zellformat_change(JSON.stringify(newArr)));
  }

  return (
    <div>
      {currentCells !== null && (
        <div>
          {/*<button onClick={()=> dispatch(zellformat_change(currentCells))}>Klick me</button>*/}

          <div style={{ width: 400 }}>
            <Dropdown
              className="zellformate__dropdown"
              id="default"
              //  titleText="Zelltypen"
              helperText="This is some helper text"
              label="Dropdown menu options"
              items={[
                ...new Set(
                  JSON.parse(currentCells).map(item => item.Zellformat)
                ),
              ]}
              onChange={
                ({ selectedItem }) =>
                  setCurrentZellformate(selectedItem) &
                  dispatch(zellformat_change(null))
                //& setMountFalse()
              }
              selectedItem={currentZellformate}
            />
          </div>

          <div className="zellformate__radiobuttons" onChange={Zell_handler}>
            {JSON.parse(currentCells).map(item =>
              item.Zellformat === currentZellformate ? (
                <div key={item.id}>
                  <input
                    key={item.id}
                    type="radio"
                    value={item.Dateiname}
                    name="Zellformat"
                  />
                  <span>{item.Beschreibung}</span>{' '}
                </div>
              ) : (
                <span key={item.id} hidden={true} />
              )
            )}
          </div>

          {zellformat !== null && (
            <div>
              <h3>{zellformatName}</h3>
              <Table useZebraStyles size="compact">
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
                  {JSON.parse(zellformat).map(item =>
                    item.Wert == null ? (
                      <TableRow key={item.id} hidden />
                    ) : (
                      <TableRow key={item.id}>
                        <TableCell>{item.Beschreibung}</TableCell>
                        <TableCell key={item.id}>
                          <NumberInput
                            size="sm"
                            id="carbon-number"
                            invalidText="Ungültiger Wert"
                            value={item.Wert}
                            onChange={e =>
                              handleChange(
                                item.Beschreibung,
                                e.imaginaryTarget.value
                              )
                            }
                          />
                        </TableCell>
                        <TableCell>{item.Einheit}</TableCell>
                      </TableRow>
                    )
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
