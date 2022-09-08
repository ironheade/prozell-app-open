import { Dropdown } from 'carbon-components-react';
import React, { useEffect, useState } from 'react';
import tabelle_abrufen from '../../../functions/tabelle_abrufen';

export default function DatenbankAdd() {
  const [zellformate, setZellformate] = useState(null);

  useEffect(() => {
    tabelle_abrufen('Zellformate').then(data =>
      setZellformate(JSON.parse(data))
    );
  }, []);

  return (
    <>
      <h1>Zellformat hinzufügen</h1>
      {zellformate !== null && (
        <Dropdown
          id="default"
          label="Zellformat"
          //items={props.dropDownData}
          items={Array.from(new Set(zellformate.map(item => item.Zellformat)))}
        />
      )}
      {zellformate !== null &&
        console.log(
          Array.from(new Set(zellformate.map(item => item.Zellformat)))
        )}
    </>
  );
}
