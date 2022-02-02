import React, { useState, useEffect } from 'react';
import { Dropdown } from 'carbon-components-react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
} from 'carbon-components-react';
//import './../_zellauslegung.scss'

export default function Zellformate() {
  //Liste der aktuell auswählbaren Zellen
  const [currentCells, setCurrentCells] = useState(null);
  //Liste aller Möglichen Zellformate
  const [currentZellformat, setCurrentZellformat] = useState('Pouchzelle');
  //Infos zur aktuell ausgewählten Zelle (Maße, etc.)
  const [Zellinfo, setZellinfo] = useState(null);

  //ruft die Tabelle aller möglichen Zelltypen aus der Datenbank ab
  useEffect(() => {
    fetch('/Zellformate')
      .then(res => res.json())
      .then(data => {
        setCurrentCells(data.Zellformate);
      });
  }, []);

  //ruft nach Auswahl der Zelle die Informationen zur Zelle aus der Datenbank ab
  const Zell_handler = event => {
    const value = event.target.value;
    fetch('/Zellwahl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Zelle: value,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setZellinfo(data.Zellinfo);
        console.log(JSON.parse(Zellinfo));
      });
  };

  //aktualisiert den state zur aktuell ausgewählten Zelle
  function handleChange(event) {
    const newArr = JSON.parse(Zellinfo).map(obj => {
      if (obj.id === parseInt(event.target.id)) {
        return { ...obj, Werte: parseInt(event.target.value) };
      }
      return obj;
    });
    setZellinfo(JSON.stringify(newArr));
  }

  return (
    <div>
      {currentCells === null ? null : (
        <div>
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
              onChange={({ selectedItem }) =>
                setCurrentZellformat(selectedItem) & setZellinfo(null)
              }
              selectedItem={currentZellformat}
            />
          </div>

          <div className="zellformate__radiobuttons" onChange={Zell_handler}>
            {JSON.parse(currentCells).map(item =>
              item.Zellformat == currentZellformat ? (
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

          {Zellinfo === null ? (
            <p />
          ) : (
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
                {JSON.parse(Zellinfo).map(item => (
                  <TableRow key={item.id}>
                    <TableCell>{item.Beschreibung}</TableCell>
                    <TableCell>
                      <input
                        value={item.Werte}
                        onChange={handleChange}
                        id={item.id}
                      />
                    </TableCell>
                    <TableCell>{item.Werte}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>
      )}
    </div>
  );
}
