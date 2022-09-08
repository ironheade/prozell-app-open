import { Button, Tab, Tabs } from 'carbon-components-react';
import React, { useEffect, useState } from 'react';
import tabelle_abrufen from '../../../functions/tabelle_abrufen';
import DatenbankTable from './DatenbankTable';

export default function Datenbank() {
  //Alle Tabellen
  const [allTables, setAllTables] = useState(null);
  const [zellformate, setZellformate] = useState(null);
  const [materialien, setMaterialen] = useState(null);
  const [prozessschritte, setProzessschritte] = useState(null);
  const [prozessrouten, setProzessrouten] = useState(null);
  const [zellchemien, setZellchemien] = useState(null);

  useEffect(() => {
    tabelle_abrufen('Zellformate').then(data =>
      setZellformate(JSON.parse(data))
    );
    tabelle_abrufen('materialien').then(data =>
      setMaterialen(JSON.parse(data))
    );
    tabelle_abrufen('prozessschritte').then(data =>
      setProzessschritte(JSON.parse(data))
    );
    tabelle_abrufen('prozessrouten').then(data =>
      setProzessrouten(JSON.parse(data))
    );
    tabelle_abrufen('Zellchemien').then(data =>
      setZellchemien(JSON.parse(data))
    );
    //fetch('/all_tables').then(res => res.json()).then(data => setAllTables(data.tables));
  }, []);
  /*
    useEffect(() => {
        fetch('/all_tables')
            .then(res => res.json())
            .then(data => {
                setAllTables(data.tables);
            });
    }, []);
*/
  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ display: 'inline-block' }}>
        <Tabs style={{ marginBottom: '20px' }}>
          {/*<Tab label="Gesamte Datenbank">
                        {allTables !== null &&
                        <DatenbankTable dropDownData={allTables} title="Alle Tabellen"/>}
                        </Tab>*/}
          <Tab label="Prozessschritte">
            {prozessschritte !== null && (
              <DatenbankTable
                dropDownData={prozessschritte}
                title="Alle Prozessschritte"
              />
            )}
          </Tab>
          <Tab label="Zellformate">
            {zellformate !== null && (
              <DatenbankTable
                dropDownData={zellformate}
                title="Alle Zellformate"
              />
            )}
          </Tab>
          <Tab label="Materialien">
            {materialien !== null && (
              <DatenbankTable
                dropDownData={materialien}
                title="Alle Materialien"
              />
            )}
          </Tab>
          <Tab label="Prozessrouten">
            {prozessrouten !== null && (
              <DatenbankTable
                dropDownData={prozessrouten}
                title="Alle Prozessrouten"
              />
            )}
          </Tab>
          <Tab label="Allgemeine Paramter">
            <DatenbankTable
              dropDownData={[
                {
                  Beschreibung: 'Ökonomische Parameter',
                  Dateiname: 'oekonomische_parameter',
                },
                { Beschreibung: 'Gebäude', Dateiname: 'gebaeude_parameter' },
                {
                  Beschreibung: 'Mitarbeiter & Logistik',
                  Dateiname: 'mitarbeiter_logistik',
                },
                { Beschreibung: 'Rückgewinnung', Dateiname: 'rueckgewinnung' },
              ]}
              title="Quellen"
            />
          </Tab>
          <Tab label="Zellchemien">
            {zellchemien !== null && (
              <DatenbankTable
                dropDownData={zellchemien}
                title="Alle Zellchemien"
              />
            )}
          </Tab>
          <Tab label="Quellen">
            <DatenbankTable
              dropDownData={[{ Beschreibung: 'Quellen', Dateiname: 'quellen' }]}
              title="Quellen"
            />
          </Tab>
        </Tabs>
      </div>
    </div>
  );
}
