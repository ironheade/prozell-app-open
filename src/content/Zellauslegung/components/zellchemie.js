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

export default function Zellchemie() {
  const [materialien, setmaterialen] = useState(null);

  //ruft die Tabelle aller möglichen Zelltypen aus der Datenbank ab
  useEffect(() => {
    fetch('/Zellmaterialien')
      .then(res => res.json())
      .then(data => {
        setmaterialen(data.Zellmaterialien);
      });
  }, []);

  function hinzu() {
    setprobezelle([...probezelle, zusatz[0]]);
    console.log(JSON.parse(materialien));
  }
  function weg() {
    console.log(probezelle);
    var newArray = [...probezelle];
    console.log(newArray);
    var index = newArray.findIndex(obj => obj.id === 4);
    if (index !== -1) {
      newArray.splice(index, 1);
      setprobezelle(newArray);
    }
  }

  function delete_(Beschreibung_delete) {
    var newArray = [...JSON.parse(materialien)];
    var index = newArray.findIndex(
      obj => obj.Beschreibung === Beschreibung_delete
    );
    if (index !== -1) {
      newArray.splice(index, 1);
      setmaterialen(JSON.stringify(newArray));
    }
  }

  const [zusatz, setzusatz] = useState([
    {
      id: 9,
      Beschreibung: 'NCM 811',
      Kategorie: 'Aktivmaterial Kathode',
      Dateiname: 'NCM_811',
    },
  ]);

  const [probezelle, setprobezelle] = useState([
    {
      id: 1,
      Beschreibung: 'NCM 622',
      Kategorie: 'Aktivmaterial Kathode',
      Dateiname: 'NCM_622',
    },
    {
      id: 2,
      Beschreibung: 'Zusatz 1',
      Kategorie: 'Zusatzmaterial Kathode',
      Dateiname: 'zusatz_1',
    },
    {
      id: 3,
      Beschreibung: 'Zusatz 2',
      Kategorie: 'Zusatzmaterial Kathode',
      Dateiname: 'zusatz_2',
    },
    {
      id: 4,
      Beschreibung: 'Aluminium',
      Kategorie: 'Folie',
      Dateiname: 'aluminium',
    },
    { id: 5, Beschreibung: 'Elyt', Kategorie: 'Elektrolyt', Dateiname: 'elyt' },
  ]);
  const [newmaterial, setnewmaterial] = useState('');

  return (
    <div>
      <p>Zellchemie</p>
      {probezelle.map(item => (
        <p key={item.id}>{item.Beschreibung}</p>
      ))}
      <input
        value={newmaterial}
        onChange={evt => setnewmaterial(evt.target.value)}
      />
      <button onClick={hinzu}>hinzufügen</button>
      <button onClick={weg}>entfernen</button>

      {materialien === null ? (
        <p />
      ) : (
        <Table useZebraStyles size="compact">
          <TableHead>
            <TableRow>
              <TableHeader>
                <p>Beschreibung</p>
              </TableHeader>
              <TableHeader>
                <p>Kategorie</p>
              </TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {JSON.parse(materialien).map(item => (
              <TableRow key={item.id}>
                <TableCell>{item.Beschreibung}</TableCell>
                <TableCell>{item.Kategorie}</TableCell>
                <TableCell>
                  <button
                    key={item.id}
                    onClick={() => delete_(item.Beschreibung)}>
                    delete
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      <br />

      <Table useZebraStyles size="compact">
        <TableHead>
          <TableRow>
            <TableHeader>
              <p>Beschreibung</p>
            </TableHeader>
            <TableHeader>
              <p>Kategorie</p>
            </TableHeader>
            <TableHeader>
              <p>Kategorie</p>
            </TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>bla</TableCell>
            <TableCell>bla</TableCell>
            <TableCell>bla</TableCell>
          </TableRow>
          <h4>new bla</h4>
          <TableRow>
            <TableCell>bla</TableCell>
            <TableCell>bla</TableCell>
            <TableCell>bla</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <p>{materialien}</p>
    </div>
  );
}
