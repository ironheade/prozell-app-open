import React, { useState, useEffect } from 'react';
import { Dropdown } from 'carbon-components-react';
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
  //Liste der aktuell auswählbaren Zellen
  const [currentCells, setCurrentCells] = useState(null);
  //Liste aller Möglichen Zellformate
  const [currentZellformate, setCurrentZellformate] = useState('Pouchzelle');
  //Infos zur aktuell ausgewählten Zelle (Maße, etc.)
  const [Zellinfo, setZellinfo] = useState(null);
  //Aktuell ausgewähltes Zellformat
  const [currentZellformat, setCurrentZellformat] = useState(null);

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
    setCurrentZellformat(
      JSON.parse(currentCells).filter(item => item.Dateiname == value)[0]
        .Beschreibung
    );
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
                setCurrentZellformate(selectedItem) & setZellinfo(null)
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

          {Zellinfo === null ? (
            <p />
          ) : (
            <div>
              <h3>{currentZellformat}</h3>
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
                  {JSON.parse(Zellinfo).map(item =>
                    item.Werte == null ? (
                      <TableRow key={item.id} hidden />
                    ) : (
                      <TableRow key={item.id}>
                        <TableCell>{item.Beschreibung}</TableCell>
                        <TableCell key={item.id}>
                          <NumberInput
                            size="sm"
                            id="carbon-number"
                            //onChange={(e) => props.onChange(props.header, item.Beschreibung, e.imaginaryTarget.value)}
                            invalidText="Ungültiger Wert"
                            value={item.Werte}
                            onChange={handleChange}
                            //id={item.id}
                          />

                          {/*
                        <input
                          value={item.Werte}
                          onChange={handleChange}
                          id={item.id}
                        />
                      */}
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
