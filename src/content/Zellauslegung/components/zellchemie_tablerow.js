import React from 'react';
import {
  TableRow,
  TableCell,
  TableBody,
  Dropdown,
  Button,
  NumberInput,
} from 'carbon-components-react';
import { SubtractAlt32 } from '@carbon/icons-react';

export default function Zellchemie_TableRow(props) {
  var listOfUsedMaterials = JSON.parse(props.Zellchemie)
    .filter(item => item.Kategorie === props.filter)
    .map(item => item.Beschreibung); //Auflistung aller genutzten Materialien einer Kategorie, für die Filterung später
  var items = JSON.parse(props.materialien) //alle Materialien
    .filter(item => item.Kategorie === props.filter) //alle Materialien der passenden Kategorie
    .filter(item =>
      listOfUsedMaterials.includes(item.Beschreibung) ? false : true
    ) //Herausfiltern aller bereits genutzten Materialien, siehe oben
    .map(item => item.Beschreibung);
  //  items.length == 0 ? console.log("empty"): console.log("not empty")
  items.length == 0 ? (items = []) : (items = items);

  return (
    <TableBody>
      <TableRow>
        <TableCell style={{ backgroundColor: 'white' }} />
        <TableCell>
          <h4>{props.filter}</h4>
        </TableCell>
        <TableCell />
        <TableCell>
          {items.length == 0 ? (
            <p />
          ) : (
            <Dropdown
              id={props.filter}
              label="weitere Materialien"
              items={items}
              onChange={event => props.onChange(event.selectedItem)}
            />
          )}
        </TableCell>
      </TableRow>
      {JSON.parse(props.Zellchemie)
        .filter(item => item.Kategorie === props.filter)
        .map(item => (
          <TableRow key={item.id}>
            <TableCell
              style={{ backgroundColor: 'white', boder: '2px solid black' }}>
              {props.unique === true ? (
                <p />
              ) : (
                <Button
                  renderIcon={SubtractAlt32}
                  hasIconOnly
                  kind="danger--tertiary"
                  iconDescription="Material entfernen"
                  key={item.id}
                  onClick={() => props.onClick(item.Beschreibung)}
                />
              )}
            </TableCell>
            <TableCell>{item.Beschreibung}</TableCell>

            <TableCell key={item.id}>
              {props.Anteil == false ? (
                <p />
              ) : (
                <NumberInput
                  size="sm"
                  id="carbon-number"
                  min={0}
                  max={100}
                  value={item.Anteil == null ? 0 : item.Anteil}
                  onChange={e =>
                    props.onIncrement(
                      item.Beschreibung,
                      e.imaginaryTarget.value
                    )
                  }
                  invalidText="Ungültiger Wert"
                />
              )}
            </TableCell>
            <TableCell />
          </TableRow>
        ))}
    </TableBody>
  );
}
